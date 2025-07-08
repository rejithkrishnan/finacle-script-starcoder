import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
import sys

# --- 1. Configure 4-bit Quantization (No changes) ---
print("Configuring 4-bit quantization...")
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)
print("Done.")

# --- 2. Load the Base Model, Tokenizer, and LoRA Adapter (No changes) ---
print("Loading the models... This may take a moment.")
base_model_name = "deepseek-ai/deepseek-coder-6.7b-instruct"
adapter_path = "./qlora-finetuned-deepseek-7b"

base_model = AutoModelForCausalLM.from_pretrained(
    base_model_name, quantization_config=bnb_config, device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(base_model_name)
model = PeftModel.from_pretrained(base_model, adapter_path)
print("\n--- Finacle Script Generator is Ready ---")
print("Type your request below, or type 'exit' or 'quit' to end the session.")

# --- 3. Define the System Prompt ---
# This instruction will be sent to the model with every user prompt.
system_prompt = "You are an expert Finacle script developer. Your task is to generate clean, correct, and complete Finacle scripts based on the user's request. Always enclose the script within <--start and end--> tags. Do not add any explanations or markdown formatting."


# --- 4. Generation Logic in a Loop ---
while True:
    try:
        prompt_text = input("\nYour Prompt > ")
    except KeyboardInterrupt:
        print("\nExiting...")
        break

    if prompt_text.lower() in ["exit", "quit"]:
        print("Exiting...")
        break

    # --- Use the chat template to combine the system and user prompts ---
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt_text},
    ]
    formatted_prompt = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    inputs = tokenizer(formatted_prompt, return_tensors="pt")
    input_ids = inputs.input_ids.to(model.device)
    attention_mask = inputs.attention_mask.to(model.device)

    with torch.no_grad():
        output = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_new_tokens=256,  # Increased slightly for longer scripts
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id,
        )

    # Decode only the newly generated part of the sequence
    output_sequence = output[0][input_ids.shape[-1] :]
    generated_text = tokenizer.decode(output_sequence, skip_special_tokens=True)

    print("\n--- Generated Finacle Script ---")
    print(generated_text.strip())
    print("--------------------------------")
