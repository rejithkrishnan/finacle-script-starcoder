import json
import yaml


# --- This new class tells the YAML library how to format multi-line strings ---
class LiteralDumper(yaml.Dumper):
    def represent_scalar(self, tag, value, style=None):
        if "\n" in value:
            style = "|"  # Use the literal block style for multi-line strings
        return super().represent_scalar(tag, value, style)


input_json_path = "training_data.json"
output_yaml_path = "editable_data.yml"

try:
    with open(input_json_path, "r", encoding="utf-8") as f_in:
        data = json.load(f_in)

    with open(output_yaml_path, "w", encoding="utf-8") as f_out:
        # We now pass our custom Dumper to the dump() function
        yaml.dump(
            data,
            f_out,
            Dumper=LiteralDumper,
            default_flow_style=False,
            sort_keys=False,
            indent=2,
            allow_unicode=True,
        )

    print(
        f"Success! Converted {len(data)} examples to '{output_yaml_path}' with clean multi-line formatting."
    )
    print("You can now edit the .yml file.")

except FileNotFoundError:
    print(f"Error: The file '{input_json_path}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
