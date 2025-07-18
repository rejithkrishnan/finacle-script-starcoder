import requests
import json

# The URL of the vLLM OpenAI-compatible endpoint
VLLM_API_URL = "http://localhost:8000/v1/completions"

# Define the headers for the API request
headers = {"Content-Type": "application/json"}

print("\n--- Finacle Script Generator (vLLM Powered) is Ready ---")
print("Type your request below, or type 'exit' or 'quit' to end the session.")

# --- Interactive Chat Loop ---
while True:
    try:
        prompt_text = input("\nYour Prompt > ")
    except KeyboardInterrupt:
        print("\nExiting...")
        break

    if prompt_text.lower() in ["exit", "quit"]:
        print("Exiting...")
        break

    # Format the prompt using the simple template
    formatted_prompt = f"PROMPT: {prompt_text}\nSCRIPT:"
    
    # --- API Payload ---
    # Create the JSON payload for the vLLM server
    payload = {
        "model": "./merged-finacle-model", # The model name/path
        "prompt": formatted_prompt,
        "max_tokens": 512,       # Max length of the generated response
        "temperature": 0.1,      # Use a low temperature for code generation
        "stop": ["<|endoftext|>"] # Tell the model when to stop
    }

    print("Generating response...")
    
    try:
        # Make the POST request to the vLLM server
        response = requests.post(VLLM_API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an exception for bad status codes

        # Parse the JSON response
        data = response.json()
        generated_text = data['choices'][0]['text']

        print("\n--- Model Response ---")
        print(generated_text.strip())
        print("--------------------------------")

    except requests.exceptions.RequestException as e:
        print(f"\nError connecting to vLLM server: {e}")