import torch
import requests
import json
import re
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

# --- MCP Server Configuration ---
MCP_SERVER_URL = "http://127.0.0.1:5000"


def get_account_context(account_id):
    """Calls the MCP server to get context for an account."""
    try:
        response = requests.get(f"{MCP_SERVER_URL}/tools/validate_account/{account_id}")
        if response.status_code == 200:
            return f"Context for account {account_id}: The account is found and its details are {json.dumps(response.json())}."
        else:
            return f"Context for account {account_id}: Account not found."
    except requests.ConnectionError:
        return "Error: Could not connect to MCP server."


def get_userhook_context(hook_name):
    """Calls the MCP server to get context for a userhook."""
    try:
        response = requests.get(
            f"{MCP_SERVER_URL}/tools/get_userhook_params/{hook_name}"
        )
        if response.status_code == 200:
            return f"Context for userhook {hook_name}: The hook details are {json.dumps(response.json())}."
        else:
            return f"Context for userhook {hook_name}: Userhook not found."
    except requests.ConnectionError:
        return "Error: Could not connect to MCP server."


# --- Model Loading (No changes) ---
print("Configuring 4-bit quantization...")
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)
print("Done.")
print("Loading the models... This may take a moment.")
base_model_name = "deepseek-ai/deepseek-coder-6.7b-instruct"
adapter_path = "./qlora-finetuned-deepseek-7b"
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_name, quantization_config=bnb_config, device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(base_model_name)
model = PeftModel.from_pretrained(base_model, adapter_path)
print("\n--- Finacle Script Generator (MCP-Enabled) is Ready ---")
print("Type your request below, or type 'exit' or 'quit' to end the session.")


# --- Interactive Chat Loop (UPDATED) ---
while True:
    prompt_text = input("\nYour Prompt > ")

    if prompt_text.lower() in ["exit", "quit"]:
        print("Exiting...")
        break

    # --- MCP Client Logic to get context ---
    system_prompt_context = ""

    # Simple regex to find account IDs or userhook names
    account_match = re.search(r"\b(SBA\w+|CAA\w+)\b", prompt_text, re.IGNORECASE)
    userhook_match = re.search(r"\b(urhk_\w+)\b", prompt_text, re.IGNORECASE)

    if account_match:
        account_id = account_match.group(1)
        print(f"MCP Client: Detected account ID '{account_id}'. Fetching context...")
        system_prompt_context += get_account_context(account_id) + " "

    if userhook_match:
        hook_name = userhook_match.group(1)
        print(f"MCP Client: Detected userhook '{hook_name}'. Fetching context...")
        system_prompt_context += get_userhook_context(hook_name)

    # --- Intent Detection and Dynamic System Prompt ---
    code_generation_keywords = ["script", "generate", "write a", "create a program"]
    intent = "Youtubeing"
    for keyword in code_generation_keywords:
        if keyword in prompt_text.lower():
            intent = "code_generation"
            break

    if intent == "code_generation":
        system_prompt = f"You are an expert Finacle script developer. Your task is to generate a complete and correct Finacle script. {system_prompt_context} Your output must only be the raw code, starting with <--start and ending with end-->."
    else:
        system_prompt = f"You are a helpful Finacle assistant. Answer the user's question directly based on the provided context. {system_prompt_context} Do not generate code unless explicitly asked."

    # --- Prompt Formatting and Generation (No changes) ---
    print(f"system: {system_prompt}\n user : {prompt_text}")
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
            max_new_tokens=1024,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id,
        )

    output_sequence = output[0][input_ids.shape[-1] :]
    generated_text = tokenizer.decode(output_sequence, skip_special_tokens=True)

    print("\n--- Model Response ---")
    print(generated_text.strip())
    print("--------------------------------")
