import json


def convert_jsonl_to_json(input_file_path, output_file_path):
    """
    Converts a JSONL file to a JSON file with a specific format.

    Args:
        input_file_path (str): The path to the input JSONL file.
        output_file_path (str): The path where the output JSON file will be saved.
    """
    # This list will hold all the converted JSON objects
    formatted_data = []

    try:
        # Open the input JSONL file for reading
        with open(input_file_path, "r", encoding="utf-8") as infile:
            # Iterate over each line in the file
            for line in infile:
                # Skip any blank lines
                if not line.strip():
                    continue

                # Load the JSON object from the current line
                try:
                    data = json.loads(line)

                    # Create a new dictionary with the desired keys
                    # It maps 'input_text' to 'prompt' and 'output_text' to 'script'
                    new_entry = {
                        "prompt": data.get("input_text"),
                        "script": data.get("output_text"),
                    }

                    # Add the newly formatted dictionary to our list
                    formatted_data.append(new_entry)

                except json.JSONDecodeError as e:
                    print(f"Skipping a line due to a JSON decoding error: {e}")

        # Open the output JSON file for writing
        with open(output_file_path, "w", encoding="utf-8") as outfile:
            # Write the entire list of formatted data to the file
            # 'indent=4' makes the JSON file human-readable
            json.dump(formatted_data, outfile, indent=4)

        print(f"Successfully converted {input_file_path} to {output_file_path}")

    except FileNotFoundError:
        print(f"Error: The file '{input_file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# --- --- --- --- --- --- --- ---
# How to use the function
# --- --- --- --- --- --- --- ---

if __name__ == "__main__":
    # Define the input and output file paths
    # Make sure 'mrt_explanation_additional.txt' is in the same directory
    # as this Python script, or provide the full path to it.

    import glob
    import os

    # Get all .jsonl files in the current directory
    jsonl_files = glob.glob("*.jsonl")

    for input_file in jsonl_files:
        # Create an output file name based on the input file name
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}_converted.json"
        convert_jsonl_to_json(input_file, output_file)
