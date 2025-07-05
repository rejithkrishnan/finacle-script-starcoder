import json
import torch
from torch.utils.data import Dataset
from transformers import (
    GPT2Tokenizer,
    GPT2LMHeadModel,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling,
)


# --- 1. Define a Custom Dataset (Corrected) ---
# The dataset now correctly handles tokenization before passing data to the collator.
class FinacleScriptDataset(Dataset):
    def __init__(self, file_path, tokenizer):
        self.tokenizer = tokenizer
        self.examples = []

        with open(file_path, "r") as f:
            data = json.load(f)

        for item in data:
            text = f"PROMPT: {item['prompt']}\nSCRIPT: {item['script']}{self.tokenizer.eos_token}"
            # We tokenize here and store the dictionary of 'input_ids', etc.
            tokenized_text = self.tokenizer(text, truncation=True, max_length=128)
            self.examples.append(tokenized_text)

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, i):
        return self.examples[i]


# --- 2. Load Tokenizer and Model ---
print("Loading model and tokenizer...")
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
# The model needs to be resized to include the new pad token
model.resize_token_embeddings(len(tokenizer))

# --- 3. Prepare the Dataset ---
print("Preparing dataset...")
train_file_path = "training_data.json"
train_dataset = FinacleScriptDataset(file_path=train_file_path, tokenizer=tokenizer)

# --- 4. Define the Data Collator ---
# This collator will now correctly receive pre-tokenized data and just handle padding.
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,
)

# --- 5. Define Training Arguments ---
training_args = TrainingArguments(
    output_dir="./fine-tuned-model",
    num_train_epochs=10,  # Increased epochs for better learning on a small dataset
    per_device_train_batch_size=1,
    warmup_steps=10,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=5,
    # This will disable the pin_memory warning
    dataloader_pin_memory=False,
)

# --- 6. Create the Trainer and Start Training ---
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=None,
    data_collator=data_collator,
)

print("Starting the fine-tuning process...")
trainer.train()
print("Training complete!")

# --- 7. Save the Final Model ---
print("Saving the fine-tuned model...")
trainer.save_model("./fine-tuned-model")
print("Model saved successfully.")
