from transformers import GPT2Tokenizer, GPT2LMHeadModel

# --- 1. Load the fine-tuned model and tokenizer ---
print("Loading the fine-tuned model...")
model_path = "./fine-tuned-model"
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
model = GPT2LMHeadModel.from_pretrained(model_path)
print("Model loaded successfully.")

# --- 2. Define the prompt ---
# This is the instruction for the model. Try changing it to test different scenarios.
prompt_text = "Write a script that subtracts 5 from 20 and prints the result."

# Format the prompt exactly as we did during training
formatted_prompt = f"PROMPT: {prompt_text}\nSCRIPT:"

# --- 3. Generate the script ---
# Tokenize the formatted prompt
input_ids = tokenizer.encode(formatted_prompt, return_tensors="pt")

print("\nGenerating script...")
# Use the model's generate() method
output = model.generate(
    input_ids,
    max_length=150,  # Maximum length of the generated text
    num_beams=5,  # Beam search can produce better results
    no_repeat_ngram_size=2,  # Prevents the model from repeating itself
    early_stopping=True,  # Stops when an end-of-sequence token is generated
    pad_token_id=tokenizer.eos_token_id,  # Set pad token id
)

# --- 4. Decode and print the result ---
# Decode the generated token IDs back into text
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

# Clean up the output to only show the generated script
# We find where "SCRIPT:" ends and take the text after that.
script_part = generated_text.split("SCRIPT:")[1].strip()

print("\n--- Generated Finacle Script ---")
print(script_part)
print("--------------------------------")
