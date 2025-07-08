import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

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
print("\n--- Finacle Script Generator is Ready (with Context) ---")
print(
    "Type your request below, or type 'exit', 'quit', or 'clear' to start a new conversation."
)

# --- 3. Interactive Chat Loop with History ---

chat_history = []

while True:
    prompt_text = input("\nYour Prompt > ")

    if prompt_text.lower() in ["exit", "quit"]:
        print("Exiting...")
        break

    if prompt_text.lower() == "clear":
        chat_history = []
        print("Conversation history cleared.")
        continue

    chat_history.append({"role": "user", "content": prompt_text})

    formatted_prompt = tokenizer.apply_chat_template(
        chat_history, tokenize=False, add_generation_prompt=True
    )

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    inputs = tokenizer(formatted_prompt, return_tensors="pt")
    input_ids = inputs.input_ids.to(model.device)
    attention_mask = inputs.attention_mask.to(model.device)

    print("Generating response...")

    with torch.no_grad():
        output = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_new_tokens=256,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id,
        )

    full_response_text = tokenizer.decode(output[0], skip_special_tokens=True)

    try:
        # --- CORRECTED LOGIC ---
        # Find the last '### Response:' marker to get the latest answer
        assistant_response = full_response_text.rsplit("### Response:", 1)[1].strip()

    except IndexError:
        assistant_response = "Could not generate a valid response."

    print("\n--- Model Response ---")
    print(assistant_response)
    print("--------------------------------")

    chat_history.append({"role": "assistant", "content": assistant_response})
