import json
import torch
from torch.utils.data import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling,
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


# --- 2. Load Base Model and Tokenizer (No changes) ---
print("Loading base model and tokenizer...")
model_name = "bigcode/starcoder2-3b"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
print("Done.")

# --- 3. Configure and Apply LoRA (No changes) ---
print("Configuring LoRA adapter...")
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=8,
    lora_alpha=32,
    lora_dropout=0.1,
    bias="none",
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
    ],
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
print("Done.")

# --- 4. Prepare Dataset and Collator (No changes) ---
print("Preparing dataset...")
train_file_path = "training_data.json"
train_dataset = FinacleScriptDataset(file_path=train_file_path, tokenizer=tokenizer)
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
print("Done.")

# --- 5. Training Arguments (KEY CHANGE HERE) ---
training_args = TrainingArguments(
    output_dir="./lora-finetuned-starcoder2-3b",
    num_train_epochs=50,
    per_device_train_batch_size=1,
    learning_rate=5e-5,
    warmup_steps=10,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=len(train_dataset),
    dataloader_pin_memory=False,
    fp16=True,  # <<<< ENABLE MIXED-PRECISION TRAINING
)

# --- 6. Trainer and Training (No changes) ---
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    data_collator=data_collator,
)

print("Starting optimized LoRA fine-tuning on starcoder2-3b...")
trainer.train()
print("Training complete!")

# --- 7. Save the LoRA Adapter (No changes) ---
print("Saving the LoRA adapter...")
model.save_pretrained("./lora-finetuned-starcoder2-3b")
tokenizer.save_pretrained("./lora-finetuned-starcoder2-3b")
print("Model and tokenizer saved.")
