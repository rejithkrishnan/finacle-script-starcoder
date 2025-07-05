import json

# The name of the JSON file to read
input_filepath = "training_data.json"
# The name of the new Markdown file to write the output to
output_filepath = "readable_training_data.md"

try:
    # Open and load the JSON data
    with open(input_filepath, "r") as f_in:
        training_data = json.load(f_in)

    # Open the output file for writing
    with open(output_filepath, "w") as f_out:
        # Write the main title for the Markdown file
        f_out.write("# Finacle Training Data Set\n\n")
        f_out.write(
            f"This document contains {len(training_data)} examples used for fine-tuning the model.\n\n"
        )

        # Loop through each entry and write it in Markdown format
        for i, entry in enumerate(training_data, 1):
            prompt = entry.get("prompt", "N/A")
            script = entry.get("script", "N/A")

            # Use Markdown formatting for better readability
            f_out.write(f"## Example {i}\n\n")
            f_out.write("### Prompt\n\n")
            f_out.write(f"> {prompt}\n\n")
            f_out.write("### Expected Script\n\n")
            f_out.write(
                "```bash\n"
            )  # Using 'bash' provides generic syntax highlighting
            f_out.write(f"{script}\n")
            f_out.write("```\n\n")
            f_out.write("---\n\n")  # Add a horizontal rule to separate examples

    # Print a success message to the console
    print(
        f"Success! The formatted Markdown output has been written to '{output_filepath}'."
    )

except FileNotFoundError:
    print(f"Error: The file '{input_filepath}' was not found.")
except json.JSONDecodeError:
    print(f"Error: The file '{input_filepath}' is not a valid JSON file.")
