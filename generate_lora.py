import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

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
print("Loading the models...")
base_model_name = "bigcode/starcoder2-3b"
adapter_path = "./qlora-finetuned-starcoder2-3b"

base_model = AutoModelForCausalLM.from_pretrained(
    base_model_name, quantization_config=bnb_config, device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(base_model_name)
model = PeftModel.from_pretrained(base_model, adapter_path)
print("Models loaded and merged successfully.")


# --- 3. Generation Logic (KEY CHANGES HERE) ---
def generate_finacle_script(prompt_text):
    formatted_prompt = f"PROMPT: {prompt_text}\nSCRIPT:"

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    inputs = tokenizer(formatted_prompt, return_tensors="pt")
    input_ids = inputs.input_ids.to(model.device)
    attention_mask = inputs.attention_mask.to(model.device)

    print(f"\n---> Generating script for prompt: '{prompt_text}'")

    with torch.no_grad():
        output = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_length=200,  # Increased max_length slightly to ensure full script is generated
            num_beams=5,
            early_stopping=True,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id,
        )

    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    try:
        # Isolate the script part after the prompt
        script_part_raw = generated_text.split("SCRIPT:")[1].strip()

        # --- ROBUST POST-PROCESSING ---
        # Find the first occurrence of "end-->" and truncate everything after it
        stop_sequence = "end-->"
        stop_index = script_part_raw.find(stop_sequence)

        if stop_index != -1:
            # If "end-->" is found, take the script up to and including that sequence
            script_part_clean = script_part_raw[: stop_index + len(stop_sequence)]
        else:
            # If for some reason "end-->" isn't generated, use the raw output
            script_part_clean = script_part_raw

    except IndexError:
        script_part_clean = "Could not generate a valid script."

    print("\n--- Generated Finacle Script ---")
    print(script_part_clean)
    print("--------------------------------\n")


# --- 4. Test ---
# generate_finacle_script(
#     "Write a script that subtracts 5 from 20 and prints the result."
# )
# generate_finacle_script("Create a while loop that prints numbers from 1 to 3.")
generate_finacle_script(
    "write a script to create a repository AXIS and a class DETAILS under that repository"
)
