import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import pandas as pd
from tqdm import tqdm
import os

def test_on_synthetic_data(csv_file, dataset_name):
    torch.random.manual_seed(0)
    # Load model to GPU
    model = AutoModelForCausalLM.from_pretrained(
        "microsoft/Phi-3-mini-4k-instruct",
        device_map="cuda",
        torch_dtype="auto",
        trust_remote_code=True,
    )

    tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")

    initial_prompt = "The following CVE describes a vulnerability in one of these protocols: 'DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL', or none. Which protocol is it? If none, please specify 'none'. In your answer the only word should be the protocol or 'none'. Here is the CVE description: "
    calibrated_prompt = "Given a CVE description, classify the vulnerability based on the network protocol involved, from the following list of options: 'ARP', 'BGP', 'ICMP', 'POP3', 'DHCP', 'DNS', 'FTP', 'SMTP', 'SSL', 'SSH', or 'None'. If the CVE does not associate with any of these protocols directly, select 'None'. Provide the classification by stating only the protocol name or 'None'. Here is the CVE description: "

    prompts = {"initial_prompt_up_to_1": initial_prompt,
               "calibrated_prompt_up_to_1": calibrated_prompt}

    df = pd.read_csv(csv_file, encoding='ISO-8859-1')

    # Add a new column 'Model_Response' to the dataframe
    df['Model_Response'] = ''

    for prompt_name in prompts:
        print(f"Started processing {prompt_name}")
        prompt_initial = prompts[prompt_name]

        # Loop through each row in the original CSV, concatenate the prompt, and store the CVE-ID and response
        for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Processing rows"):
            whole_prompt = prompt_initial + row['Description']
            # Create pipeline
            pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
            )
            # Define arguments
            generation_args = {
                "max_new_tokens": 25,
                "return_full_text": False,
                "temperature": 0.0,
                "do_sample": False,
            }

            messages = [
                {"role": "system", "content": "You are a cybersecurity expert specializing in identifying network protocols related to vulnerabilities."},
                {"role": "user", "content": whole_prompt}
            ]

            output = pipe(messages, **generation_args)
            response = output[0]['generated_text']
            # if dataset_name == 'none':
            #     print(response)

            # Update the 'Model_Response' column in the dataframe
            df.at[index, 'Model_Response'] = response

        # Ensure the directory exists
        output_dir = "model_responses_synthetic"
        os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

        # Save the new dataframe to a CSV file
        output_file = os.path.join(output_dir, f"{prompt_name}_{dataset_name}.csv")
        df.to_csv(output_file, index=False)
        print(f"{prompt_name} complete")


test_on_synthetic_data("datasets/none_synthetic.csv", 'none')
test_on_synthetic_data("datasets/single_synthetic.csv", 'single')