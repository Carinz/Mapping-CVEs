# Set up your OpenAI API key
KEY = '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'

from openai import OpenAI
client = OpenAI(api_key = KEY)

for file in ["requests_jsonl/synthetic_data/none_requests.jsonl", "requests_jsonl/synthetic_data/single_requests.jsonl"]:
    batch_input_file = client.files.create(
        file=open(file, "rb"),
        purpose="batch"
    )

    batch_input_file_id = batch_input_file.id

    batch_object = client.batches.create(
        input_file_id=batch_input_file_id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={
          "description": file
        }
    )
    print(batch_object)
