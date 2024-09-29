import json
import pandas as pd
import os

def parse_batch(input_file_path, output_file_path):
    # Initialize a list to hold the extracted data
    data = []

    # Read the JSONL file
    with open(input_file_path, 'r') as jsonl_file:
        for line in jsonl_file:
            entry = json.loads(line)
            custom_id = entry.get("custom_id")
            description_with_protocol = entry["response"]["body"]["choices"][0]["message"]["content"]

            # Split the description to get the protocol and the actual description
            protocol, description = description_with_protocol.split("\n", 1)

            # Clean the protocol name by removing spaces
            protocol_cleaned = protocol.replace(" ", "")

            # Append the extracted data to the list
            data.append({
                'CVE_ID': custom_id,
                'Description': description.strip(),  # Remove any leading/trailing whitespace
                'Protocol': protocol_cleaned
            })

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(data)

    # Write the DataFrame to a CSV file
    df.to_csv(output_file_path, index=False)

    print(f"Data has been successfully written to {output_file_path}.")


parse_batch('responses_jsonl/none_responses.jsonl', 'responses_csv/none_responses.csv')
parse_batch('responses_jsonl/single_responses.jsonl', 'responses_csv/single_responses.csv')
