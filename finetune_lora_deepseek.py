import json
import torch
from torch.utils.data import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling,
    BitsAndBytesConfig,
)
from peft import get_peft_model, LoraConfig, TaskType


# --- 1. Dataset Class (No changes) ---
class FinacleScriptDataset(Dataset):
    def __init__(self, file_path, tokenizer):
        self.tokenizer = tokenizer
        self.examples = []
        with open(file_path, "r") as f:
            data = json.load(f)
        for item in data:
            text = f"PROMPT: {item['prompt']}\nSCRIPT: {item['script']}{self.tokenizer.eos_token}"
            tokenized_text = self.tokenizer(text, truncation=True, max_length=128)
            self.examples.append(tokenized_text)

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, i):
        return self.examples[i]


# --- 2. Configure 4-bit Quantization (No changes) ---
print("Configuring 4-bit quantization...")
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)
print("Done.")

# --- 3. Load Base Model and Tokenizer (KEY CHANGE HERE) ---
print("Loading base model and tokenizer with 4-bit quantization...")
model_name = (
    "deepseek-ai/deepseek-coder-6.7b-instruct"  # <<<< UPGRADED TO DEEPSEEK CODER
)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto",  # This will automatically place the model on the GPU
)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
print("Done.")

# --- 4. Configure and Apply LoRA (No changes) ---
print("Configuring LoRA adapter...")
lora_config = LoraConfig(
    r=16,  # Increased rank for a larger model
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
    ],  # Common targets for these models
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
print("Done.")

# --- 5. Prepare Dataset and Collator (No changes) ---
print("Preparing dataset...")
train_file_path = "training_data.json"
train_dataset = FinacleScriptDataset(file_path=train_file_path, tokenizer=tokenizer)
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
print("Done.")

# --- 6. Training Arguments (KEY CHANGES HERE) ---
training_args = TrainingArguments(
    output_dir="./qlora-finetuned-deepseek-7b",
    num_train_epochs=10,  # Start with fewer epochs for such a large model
    per_device_train_batch_size=1,  # <<<< MUST BE 1
    gradient_accumulation_steps=4,  # <<<< SIMULATE BATCH SIZE OF 4
    learning_rate=2e-4,  # A common learning rate for QLoRA
    warmup_steps=10,
    logging_dir="./logs",
    logging_steps=10,
    fp16=True,  # Use mixed precision
    optim="paged_adamw_8bit",  # Use a memory-efficient optimizer
)

# --- 7. Trainer and Training ---
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    data_collator=data_collator,
)

print("Starting QLoRA fine-tuning on DeepSeek Coder 6.7B...")
trainer.train()
print("Training complete!")

# --- 8. Save the LoRA Adapter ---
print("Saving the LoRA adapter...")
model.save_pretrained("./qlora-finetuned-deepseek-7b")
tokenizer.save_pretrained("./qlora-finetuned-deepseek-7b")
print("Model and tokenizer saved.")
