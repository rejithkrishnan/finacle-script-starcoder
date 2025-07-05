from transformers import GPT2Tokenizer, GPT2LMHeadModel

# --- 1. Load the fine-tuned model and tokenizer ---
print("Loading the fine-tuned model...")
model_path = "./fine-tuned-model"
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
model = GPT2LMHeadModel.from_pretrained(model_path)
print("Model loaded successfully.")

# --- 2. Define the prompt ---
prompt_text = "Write a script that subtracts 5 from 20 and prints the result."
formatted_prompt = f"PROMPT: {prompt_text}\nSCRIPT:"

# --- 3. Generate the script ---
inputs = tokenizer(formatted_prompt, return_tensors="pt")
input_ids = inputs.input_ids
attention_mask = inputs.attention_mask

print("\nGenerating script...")
# Use the model's generate() method with new parameters for more focused output
output = model.generate(
    input_ids,
    attention_mask=attention_mask,
    max_length=150,
    num_beams=5,
    no_repeat_ngram_size=2,
    early_stopping=True,
    pad_token_id=tokenizer.eos_token_id,
    temperature=0.7,  # Makes the output less random
    top_k=50,  # Considers only the top 50 most likely words at each step
)

# --- 4. Decode and print the result ---
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

try:
    script_part = generated_text.split("SCRIPT:")[1].strip()
except IndexError:
    script_part = "Could not generate a valid script."

print("\n--- Generated Finacle Script ---")
print(script_part)
print("--------------------------------")
