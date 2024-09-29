import json
import os

prompts=[
    "Give an example of a Common Vulnerabilities and Exposures (CVE) description, where no network protocols from the following list are involved: DNS, DHCP, ICMP, BGP, SMTP, POP3, SSH, ARP, FTP, SSL. \
    Nevertheless, it should be non-trivial that no protocol from the list is involved. Your answer must start by the word 'None', then a line break, and finally the CVE description. For example:\n\
    None\n\
    A vulnerability in the authentication mechanism of the software allows an attacker to bypass security controls by exploiting a flaw in session management. By manipulating cookies used to track user sessions, an attacker can gain unauthorized access to sensitive information without proper credentials. This issue arises from inadequate validation of session tokens and insufficient measures to prevent session fixation attacks, enabling potential data breaches and unauthorized actions within the application.",
    "Give an example of a Common Vulnerabilities and Exposures (CVE) description, where exactly one network protocol is involved, but its name is not mentioned explicitly in the description. The involved protocol must be from the following list: DNS, DHCP, ICMP, BGP, SMTP, POP3, SSH, ARP, FTP, SSL. The vulnerability may be either in the protocol implementation, or in the way in which a hardware or software product utilizes the protocol. Your answer must start by stating the involved network protocol, then a line break, and finally the CVE description. For example:\n\
    POP3\n\
    A vulnerability exists in the email retrieval process, where improper input validation allows a remote attacker to execute arbitrary commands on the server. By sending a specially crafted message during the authentication phase, the attacker can exploit a buffer overflow condition, potentially gaining unauthorized access to user accounts or sensitive information. This issue stems from inadequate handling of client-supplied data during the communication handshake."
]

prompt_names = [
    "none",
    "single"
]

def create_requests_file_for_synthetic_data(prompt, prompt_name, num_samples):
    csv_file_path = 'data after manipulation/final_all.csv'
    output_dir = 'requests_jsonl/synthetic_data'
    jsonl_file_path = os.path.join(output_dir, f'{prompt_name}_requests.jsonl')

    os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
    # Open the JSONL file for writing
    with open(jsonl_file_path, mode='w', encoding='utf-8') as jsonlfile:
        # Iterate over each row in the CSV
        request_num=1
        for i in range(num_samples):
            # Prepare the content string
            jsonl_entry = {'custom_id': 'request-'+str(request_num), 'method': 'POST', 'url': '/v1/chat/completions', 'body': {'model': 'gpt-4o-mini', 'messages': [{'role': 'system', 'content': 'You are an expert in cybersecurity and vulnerability descriptions. Your task is to generate descriptions for Common Vulnerabilities and Exposures (CVE).'},{'role': 'user', 'content': prompt}],'max_tokens': 1000}}
            # Write the dictionary as a JSON object in the JSONL file
            jsonlfile.write(json.dumps(jsonl_entry) + '\n')
            request_num+=1

create_requests_file_for_synthetic_data(prompts[0], prompt_names[0], num_samples=50)
create_requests_file_for_synthetic_data(prompts[1], prompt_names[1], num_samples=50)