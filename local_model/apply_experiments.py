import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import pandas as pd
from tqdm import tqdm
import os

# Load the CSV data file
csv_file = "datasets/final_all.csv"  # Replace with your actual CSV file path

torch.random.manual_seed(0)
# Load model to GPU if possible
model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Phi-3-mini-4k-instruct",
    device_map="auto",
    torch_dtype="auto",
    trust_remote_code=True,
)

tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")

prompt_experiments=[
    "The following CVE describes a vulnerability in one of these protocols: 'DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL', or none. Which protocol is it? If none, please specify 'none'. In your answer the only word should be the protocol or 'none'. Here is the CVE description: ",
     "The following CVE describes a vulnerability in one or more of these protocols: 'DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL', or none. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) (separated by commas for more than one protocol) or 'none'. Here is the CVE description: ",
     "The following CVE describes a vulnerability in one or two protocols, or possibly none. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) (separated by commas for more than one protocol) or 'none'. Here is the CVE description: ",
     "The following CVE describes a vulnerability in one or two protocols, or possibly none. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) (separated by commas for more than one protocol) or 'none', then explain your answer. Here is the CVE description: ",
     "The following CVE describes a vulnerability in one or two of these protocols: 'DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL', or none. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) (separated by commas for more than one protocol) or 'none' then explain your answer. Here is the CVE description: ",
     "The following CVE describes a vulnerability in one or two of these protocols: 'DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL', or none. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) (separated by commas for more than one protocol) or 'none'. For example, in this CVE description the answer is none: 'IBM Jazz Foundation (IBM Rational Collaborative Lifecycle Management 5.0 through 6.0.6) is vulnerable to HTTP header injection, caused by improper validation of input. By persuading a victim to visit a specially-crafted Web page, a remote attacker could exploit this vulnerability to inject arbitrary HTTP headers, which will allow the attacker to conduct various attacks against the vulnerable system, including cross-site scripting, cache poisoning or session hijacking. IBM X-Force ID: 144884.'. In this CVE description the answer is 'DNS': 'The Microsoft Windows Domain Name System (DNS) DNSAPI.dll on Microsoft Windows 8.1, Windows Server 2012 R2, Windows RT 8.1, Windows 10 Gold, 1511, 1607, and 1703, and Windows Server 2016 allows a remote code execution vulnerability when it fails to properly handle DNS responses, aka 'Windows DNSAPI Remote Code Execution Vulnerability'. Here is the CVE description you need to answer: ",
     "The following CVE describes a vulnerability in one or two protocols, or possibly none. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) (separated by commas for more than one protocol) or 'none'. For example, in this CVE description the answer is none: 'IBM Jazz Foundation (IBM Rational Collaborative Lifecycle Management 5.0 through 6.0.6) is vulnerable to HTTP header injection, caused by improper validation of input. By persuading a victim to visit a specially-crafted Web page, a remote attacker could exploit this vulnerability to inject arbitrary HTTP headers, which will allow the attacker to conduct various attacks against the vulnerable system, including cross-site scripting, cache poisoning or session hijacking. IBM X-Force ID: 144884.'. In this CVE description the answer is 'DNS': 'The Microsoft Windows Domain Name System (DNS) DNSAPI.dll on Microsoft Windows 8.1, Windows Server 2012 R2, Windows RT 8.1, Windows 10 Gold, 1511, 1607, and 1703, and Windows Server 2016 allows a remote code execution vulnerability when it fails to properly handle DNS responses, aka 'Windows DNSAPI Remote Code Execution Vulnerability'. Here is the CVE description you need to answer: ",
     "The following CVE describes a vulnerability in one or two of these protocols: 'DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL', or none. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) (separated by commas for more than one protocol) or 'none'. Here is the CVE description: ",
     "The following CVE describes a vulnerability in one or more protocols, or possibly none. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) (separated by commas for more than one protocol) or 'none'. Here is the CVE description: ",
     "Given a CVE description, classify the vulnerability based on the network protocol involved, from the following list of options: 'ARP', 'BGP', 'ICMP', 'POP3', 'DHCP', 'DNS', 'FTP', 'SMTP', 'SSL', 'SSH', or 'None'. If the CVE does not associate with any of these protocols directly, select 'None'. Provide the classification by stating only the protocol name or 'None'. Here is the CVE description: ",
     "Review the CVE description to identify any of the following network protocols that are associated with the vulnerability: 'ARP', 'BGP', 'ICMP', 'POP3', 'DHCP', 'DNS', 'FTP', 'SMTP', 'SSL', 'SSH', 'DNS, DHCP', 'FTP, SSL', 'SMTP, POP3', 'SSH, ARP', 'ICMP, BGP'. Ensure to only associate the CVE with protocols explicitly mentioned or implicated as vulnerable. If no protocol from the list is mentioned or clearly associated with the vulnerability, choose 'None'. Your response should contain only the protocol label(s) without additional explanation or text. Here is the CVE description: "
]

experiment_names = [
    "basic_prompt_single_label",
    "basic_prompt_multilabel_no_constrictions_unranked",
    "basic_prompt_generation_up_to_2",
    "explanation_prompt_generation_up_to_2",
    "explanation_prompt_multilabel_unranked_up_to_2",
    "example_prompt_multilabel_unranked_up_to_2",
    "example_prompt_generation_up_to_2",
    "basic_prompt_multilabel_unranked_up_to_2",
    "basic_prompt_generation_no_constrictions",
    "calibrated_prompt_up_to_1",
    "calibrated_prompt_up_to_2"
]

df = pd.read_csv(csv_file, encoding='ISO-8859-1')

# Add a new column 'Model_Response' to the dataframe
df['Model_Response'] = ''

for experiment_idx, experiment_name in enumerate(experiment_names):
    print(f"Started processing {experiment_name}")
    prompt_initial = prompt_experiments[experiment_idx]

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

        # Update the 'Model_Response' column in the dataframe
        df.at[index, 'Model_Response'] = response

    # Ensure the directory exists
    output_dir = "model_responses"
    os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

    # Save the new dataframe to a CSV file
    output_file = os.path.join(output_dir, f"{experiment_name}.csv")
    df.to_csv(output_file, index=False)
    print(f"{experiment_name} complete")
