import time

import openai
import pandas as pd

# Set up your OpenAI API key
KEY = ''

from openai import OpenAI

client = OpenAI(api_key=KEY)

batch_input_file = client.files.create(
    # file=open("requests_jsonl/basic_prompt_generation_up_to_2_requests.jsonl", "rb"),
    # file=open("requests_jsonl/basic_prompt_multilabel_no_constrictions_unranked_requests.jsonl", "rb"),
    # file=open("requests_jsonl/basic_prompt_multilabel_unranked_up_to_2_requests.jsonl", "rb"),
    # file=open("requests_jsonl/example_prompt_generation_up_to_2_requests.jsonl", "rb"),
    # file=open("requests_jsonl/example_prompt_multilabel_unranked_up_to_2_requests.jsonl", "rb"),
    # file=open("requests_jsonl/explanation_prompt_generation_up_to_2_requests.jsonl", "rb"),
    # file=open("requests_jsonl/explanation_prompt_multilabel_unranked_up_to_2_requests.jsonl", "rb"),
    #   file=open("requests_jsonl/basic_prompt_generation_no_constrictions_requests.jsonl", "rb"),
    #   file=open("requests_jsonl/auto_prompt_output_requests.jsonl", "rb"),
    file=open("requests_jsonl/basic_prompt_single_label_requests.jsonl", "rb"),
    purpose="batch"
)

batch_input_file_id = batch_input_file.id

batch_object = client.batches.create(
    input_file_id=batch_input_file_id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={
        "description": "nightly eval job"
    }
)
print(batch_object)
