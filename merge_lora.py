import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import os  # <<<< Import the 'os' module

# --- Configuration ---
base_model_name = "deepseek-ai/deepseek-coder-6.7b-instruct"
adapter_path = "./qlora-finetuned-deepseek-7b"
merged_model_path = "./merged-finacle-model"
offload_dir = "./offload"  # <<<< Define a name for the temporary offload folder

# <<<< Create the offload directory if it doesn't exist >>>>
os.makedirs(offload_dir, exist_ok=True)


# --- Load Models and Tokenizer ---
print(f"Loading base model: {base_model_name}")
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_name,
    torch_dtype=torch.float16,
    device_map="auto",
)

print(f"Loading LoRA adapter: {adapter_path}")
# <<<< Add the offload_folder parameter to the function call >>>>
model = PeftModel.from_pretrained(base_model, adapter_path, offload_folder=offload_dir)
tokenizer = AutoTokenizer.from_pretrained(base_model_name)


# --- Merge and Save ---
print("Merging adapter into the base model...")
model = model.merge_and_unload()
print("Merge complete.")

print(f"Saving merged model to: {merged_model_path}")
model.save_pretrained(merged_model_path)
tokenizer.save_pretrained(merged_model_path)
print("Merged model and tokenizer saved successfully.")