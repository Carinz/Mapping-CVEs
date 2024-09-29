import json
import pandas as pd

from openai import OpenAI

KEY = ''
output_file_names = [
    'file-v8AfvBUuvgI5xdqho2NRMuQp',
    'file-arZOCg16QiEHttRxA6NBXJTg',
    'file-w5rVznykIQ0b9dCMnOrKdwhs',
    'file-TqyBSj07RNXo5FEf14DDdzpu',
    'file-Qd7cBxy0Zl7lsDwuM9WMovHf',
    'file-2NqRAZwZIp7uK0GR0JWZ74Vm',
    'file-nJJ5PiSSqYlESHw6GekgmzDm',
    'file-WyC0XFSUJijwOeDNBhBCOEgc',
    'file-36Ps5CulDr5HCfO301WmVXxR',
    'file-JaOgmNDHqG2Qhk43dgkbfeAo'
]

experiment_names = [
    "basic_prompt_generation_up_to_2",
    "basic_prompt_multilabel_no_constrictions_unranked",
    "basic_prompt_multilabel_unranked_up_to_2",
    "example_prompt_generation_up_to_2",
    "example_prompt_multilabel_unranked_up_to_2",
    "explanation_prompt_generation_up_to_2",
    "explanation_prompt_multilabel_unranked_up_to_2",
    "basic_prompt_generation_no_constrictions",
    "auto_prompt_output",
    "basic_prompt_single_label"
]

client = OpenAI(api_key=KEY)
for i in range(len(experiment_names)):
    file_response = client.files.content(output_file_names[i])
    responses = []
    # print(file_response.text)
    lines = file_response.text.split("\n")
    lines = lines[:-1]
    for line in lines:
        dict_obj = json.loads(line)
        response = dict_obj["response"]
        body = response["body"]
        choices = body["choices"]
        choices = choices[0]
        message = choices["message"]
        content = message["content"]
        responses.append(content)
    df = pd.read_csv('data after manipulation/final_all.csv', encoding='ISO-8859-1')
    df['Protocol'] = df['Protocol'].fillna('None')
    df['ChatGPT_Response'] = responses
    df.to_csv("batch_experiments/" + experiment_names[i] + '.csv', index=False)
