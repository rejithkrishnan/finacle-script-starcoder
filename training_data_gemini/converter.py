import json


def convert_json_format(input_file_path, output_file_path):
    """
    Converts a JSON file containing a list of "prompt":"script" objects
    to a JSONL file with a more structured conversational format.

    Args:
        input_file_path (str): The path to the source JSON file.
        output_file_path (str): The path where the converted JSONL file will be saved.
    """
    try:
        # Open the input and output files
        with open(input_file_path, "r", encoding="utf-8") as infile, open(
            output_file_path, "w", encoding="utf-8"
        ) as outfile:

            # Load the entire JSON array from the input file
            original_list = json.load(infile)

            # Ensure the loaded data is a list
            if not isinstance(original_list, list):
                print("Error: The input JSON file should contain a list of objects.")
                return

            # Process each object in the list
            for original_data in original_list:
                # Extract the prompt and script
                prompt_text = original_data.get("prompt")
                script_text = original_data.get("script")

                # Ensure both prompt and script exist before proceeding
                if prompt_text is None or script_text is None:
                    print(
                        f"Skipping object due to missing 'prompt' or 'script': {original_data}"
                    )
                    continue

                # Create the new structured format
                converted_data = {
                    "contents": [
                        {"role": "user", "parts": [{"text": prompt_text}]},
                        {"role": "model", "parts": [{"text": script_text}]},
                    ]
                }

                # Write the new JSON object as a string to the output file,
                # followed by a newline character to maintain the JSONL format.
                outfile.write(json.dumps(converted_data) + "\n")

        print(f"Conversion successful! Output saved to '{output_file_path}'")

    except FileNotFoundError:
        print(f"Error: The file '{input_file_path}' was not found.")
    except json.JSONDecodeError:
        print(
            f"Error: Could not decode JSON from the file '{input_file_path}'. Please ensure it's a valid JSON file."
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# --- Example Usage ---

# 1. First, create a sample input file named 'input.json'.
#    This file will contain a JSON array (a list of objects).
try:
    sample_data = [
        {
            "prompt": "Can you perform a case-insensitive string comparison?",
            "script": "Yes, the `STRICMP(Var1, Var2)` function performs a string comparison of two strings without regard to case.",
        },
        {
            "prompt": "How do I get the current date?",
            "script": "You can use the `GETDATE()` function to retrieve the current system date.",
        },
        {
            "prompt": "What is the syntax for a conditional statement?",
            "script": "The syntax is `IF (condition) THEN ... ELSE ... ENDIF`.",
        },
    ]
    with open("input.json", "w", encoding="utf-8") as f:
        json.dump(sample_data, f, indent=4)
    print("Created 'input.json' for demonstration.")
except Exception as e:
    print(f"Could not create sample file: {e}")


# 2. Now, run the conversion.
#    This will read 'input.json' and create 'output.jsonl'.

import glob
import os

# Get all JSON files in the 'training_data' directory
input_files = glob.glob(os.path.join("training_data", "*.json"))

# Parse each JSON file one by one
for input_file in input_files:
    # Derive output file name based on input file name
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = f"training_data_gemini/output_{base_name}.jsonl"
    convert_json_format(input_file, output_file)

# Consolidate all output_*.jsonl files into one single file
output_jsonl_files = glob.glob(os.path.join("training_data_gemini", "output_*.jsonl"))
consolidated_file = os.path.join("training_data_gemini", "all_training_data.jsonl")

with open(consolidated_file, "w", encoding="utf-8") as outfile:
    for fname in output_jsonl_files:
        with open(fname, "r", encoding="utf-8") as infile:
            for line in infile:
                outfile.write(line)
print(f"Consolidated {len(output_jsonl_files)} files into '{consolidated_file}'.")


# # 3. (Optional) You can print the contents of the output file to verify.
# print("\n--- Contents of output.jsonl ---")
# try:
#     with open(output_file, "r", encoding="utf-8") as f:
#         for line in f:
#             print(line.strip())
# except FileNotFoundError:
#     print("Output file not found. Run the conversion first.")
# except Exception as e:
#     print(f"An error occurred while reading the output file: {e}")
