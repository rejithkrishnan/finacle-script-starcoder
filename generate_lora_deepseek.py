import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
import sys

# --- 1. Configure 4-bit Quantization ---
print("Configuring 4-bit quantization...")
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)
print("Done.")

# --- 2. Load the Base Model, Tokenizer, and LoRA Adapter ---
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


# --- 3. Generation Logic in a Loop ---
while True:
    # Prompt the user for input
    try:
        prompt_text = input("\nYour Prompt > ")
    except KeyboardInterrupt:
        # Allow exiting with Ctrl+C
        print("\nExiting...")
        break

    # Check if the user wants to exit
    if prompt_text.lower() in ["exit", "quit"]:
        print("Exiting...")
        break

    # Format the prompt for the model
    formatted_prompt = f"PROMPT: {prompt_text}\nSCRIPT:"

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    inputs = tokenizer(formatted_prompt, return_tensors="pt")
    input_ids = inputs.input_ids.to(model.device)
    attention_mask = inputs.attention_mask.to(model.device)

    print("Generating script...")

    with torch.no_grad():
        output = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_new_tokens=200,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id,
        )

    output_sequence = output[0][input_ids.shape[-1] :]
    generated_text = tokenizer.decode(output_sequence, skip_special_tokens=True)

    print("\n--- Generated Finacle Script ---")
    print(generated_text.strip())
    print("--------------------------------")
