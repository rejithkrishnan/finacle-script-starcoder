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
import os  # <<<< Import the 'os' module for file system operations


# --- 1. Dataset Class (UPDATED) ---
# This class now loads all .json files from a directory
class FinacleScriptDataset(Dataset):
    def __init__(self, directory_path, tokenizer):
        self.tokenizer = tokenizer
        self.examples = []

        print(f"Loading all .json files from directory: {directory_path}")

        # Check if the directory exists
        if not os.path.isdir(directory_path):
            raise ValueError(f"Provided path '{directory_path}' is not a directory.")

        # Loop through all files in the specified directory
        for filename in os.listdir(directory_path):
            if filename.endswith(".json"):
                file_path = os.path.join(directory_path, filename)
                print(f"  - Loading data from: {filename}")
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        # The text formatting remains the same
                        text = f"PROMPT: {item['prompt']}\nSCRIPT: {item['script']}{self.tokenizer.eos_token}"
                        tokenized_text = self.tokenizer(
                            text, truncation=True, max_length=512
                        )
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

# --- 3. Load Base Model and Tokenizer (No changes) ---
print("Loading base model and tokenizer with 4-bit quantization...")
model_name = "deepseek-ai/deepseek-coder-6.7b-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto",
)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
print("Done.")

# --- 4. Configure and Apply LoRA (No changes) ---
print("Configuring LoRA adapter...")
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
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

# --- 5. Prepare Dataset and Collator (UPDATED) ---
print("Preparing dataset...")
# <<<< Define the directory containing your training files
train_directory_path = "training_data/"
# <<<< Instantiate the dataset with the directory path
train_dataset = FinacleScriptDataset(
    directory_path=train_directory_path, tokenizer=tokenizer
)
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
print(f"Dataset prepared with {len(train_dataset)} total examples.")
print("Done.")

# --- 6. Training Arguments (No changes) ---
training_args = TrainingArguments(
    output_dir="./qlora-finetuned-deepseek-7b",
    num_train_epochs=10,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    warmup_steps=10,
    logging_dir="./logs",
    logging_steps=10,
    fp16=True,
    optim="paged_adamw_8bit",
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
