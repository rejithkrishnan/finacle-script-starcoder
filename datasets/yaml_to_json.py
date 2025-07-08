import json
import yaml

input_yaml_path = "training_data_userhooks.yml"
output_json_path = "training_data_userhooks.json"

try:
    with open(input_yaml_path, "r", encoding="utf-8") as f_in:
        # safe_load() securely parses the YAML file into a Python object
        data = yaml.safe_load(f_in)

    # Write the Python object to the JSON file
    with open(output_json_path, "w", encoding="utf-8") as f_out:
        json.dump(data, f_out, indent=2)

    print(
        f"Success! Converted {len(data)} examples from '{input_yaml_path}' back to '{output_json_path}'."
    )
    print("Your JSON file is ready for training.")

except FileNotFoundError:
    print(f"Error: The file '{input_yaml_path}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
