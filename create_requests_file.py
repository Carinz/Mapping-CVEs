import pandas as pd

import csv
import json

prompt_experiments = [
    # In your answer only state your final protocol or protocols
    # "What are the protocols of the following CVE? Choose which ones you think apply from these protocols: 'DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL' or None. In your answer mention the protocol or protocols first. This is the CVE's description: ",
    # "Please analyze [CVE number] and determine which of the following protocols: DNS, DHCP, ICMP, BGP, SMTP, POP3, SSH, ARP, FTP, SSL or None, are relevant to it. Provide a detailed explanation for your choices, including why each selected protocol is applicable. In your response state first your final answer for the protocol or protocols then the rest of your answer. This is the CVE's description: "
    # "What protocol or protocols is this CVE about? For any protocol you mention, state your confidence in it. In your response state first your final answer for the protocol or protocols then the rest of your answer. This is the CVE's description: "
    # "Tag for the given CVE which protocol the weakness of it is about. The CVE number is [CVE number] and the CVE's description is: "
    # "What are the protocols of the following CVE? Choose which ones you think apply from these protocols: 'DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL' or None. The CVE's number is [CVE number] and this is the CVE's description: "
    # "What is the protocol of the following CVE? Choose which one you think apply best from these protocols: 'DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL' or None. Explain your answer. In your response state first your final answer for the protocol or protocols then the rest of your answer. The CVE's number is [CVE number] and this is the CVE's description: "

    ###optional##### "The following CVE describes a vulnerability in one or more of these protocols: 'DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL', or none. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) or 'none'. Additionally, rank these protocols and state your confidence level regarding the likelihood that the CVE pertains to them. Here is the CVE description: ",
    ###optional#####  "The following CVE describes a vulnerability in one or more of these protocols: 'DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL', or none. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) or 'none' then explain your answer. Additionally, rank these protocols and state your confidence level regarding the likelihood that the CVE pertains to them. Here is the CVE description: "
    ###------------------

    "The following CVE describes a vulnerability in one or more of these protocols: 'DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL', or none. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) (separated by commas for more than one protocol) or 'none'. Here is the CVE description: ",
    "The following CVE describes a vulnerability in one or two protocols, or possibly none. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) (separated by commas for more than one protocol) or 'none'. Here is the CVE description: ",
    "The following CVE describes a vulnerability in one or two protocols, or possibly none. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) (separated by commas for more than one protocol) or 'none', then explain your answer. Here is the CVE description: ",
    "The following CVE describes a vulnerability in one or two of these protocols: 'DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL', or none. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) (separated by commas for more than one protocol) or 'none' then explain your answer. Here is the CVE description: ",
    "The following CVE describes a vulnerability in one or two of these protocols: 'DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL', or none. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) (separated by commas for more than one protocol) or 'none'. For example, in this CVE description the answer is none: 'IBM Jazz Foundation (IBM Rational Collaborative Lifecycle Management 5.0 through 6.0.6) is vulnerable to HTTP header injection, caused by improper validation of input. By persuading a victim to visit a specially-crafted Web page, a remote attacker could exploit this vulnerability to inject arbitrary HTTP headers, which will allow the attacker to conduct various attacks against the vulnerable system, including cross-site scripting, cache poisoning or session hijacking. IBM X-Force ID: 144884.'. In this CVE description the answer is 'DNS': 'The Microsoft Windows Domain Name System (DNS) DNSAPI.dll on Microsoft Windows 8.1, Windows Server 2012 R2, Windows RT 8.1, Windows 10 Gold, 1511, 1607, and 1703, and Windows Server 2016 allows a remote code execution vulnerability when it fails to properly handle DNS responses, aka 'Windows DNSAPI Remote Code Execution Vulnerability'. Here is the CVE description you need to answer: ",
    "The following CVE describes a vulnerability in one or two protocols, or possibly none. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) (separated by commas for more than one protocol) or 'none'. For example, in this CVE description the answer is none: 'IBM Jazz Foundation (IBM Rational Collaborative Lifecycle Management 5.0 through 6.0.6) is vulnerable to HTTP header injection, caused by improper validation of input. By persuading a victim to visit a specially-crafted Web page, a remote attacker could exploit this vulnerability to inject arbitrary HTTP headers, which will allow the attacker to conduct various attacks against the vulnerable system, including cross-site scripting, cache poisoning or session hijacking. IBM X-Force ID: 144884.'. In this CVE description the answer is 'DNS': 'The Microsoft Windows Domain Name System (DNS) DNSAPI.dll on Microsoft Windows 8.1, Windows Server 2012 R2, Windows RT 8.1, Windows 10 Gold, 1511, 1607, and 1703, and Windows Server 2016 allows a remote code execution vulnerability when it fails to properly handle DNS responses, aka 'Windows DNSAPI Remote Code Execution Vulnerability'. Here is the CVE description you need to answer: ",
    "The following CVE describes a vulnerability in one or two of these protocols: 'DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL', or none. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) (separated by commas for more than one protocol) or 'none'. Here is the CVE description: ",
    "The following CVE describes a vulnerability in one or more protocols, or possibly none. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) (separated by commas for more than one protocol) or 'none'. Here is the CVE description: ",
    "Isolate and identify the network protocol associated with the CVE description by focusing on both explicit mentions and implicit clues within the broader context, including software names and system components. Choose from 'ARP', 'BGP', 'ICMP', 'POP3', 'DHCP', 'DNS', 'FTP', 'SMTP', 'SSL', 'SSH', or 'None' if no protocol is directly implicated. Provide only the protocol name or 'None' as your response. Here is the CVE description: ",
    "The following CVE describes a vulnerability in one of these protocols: 'DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL', or none. Which protocol is it? If none, please specify 'none'. In your answer the only word should be the protocol or 'none'. Here is the CVE description: "
]

experiment_names = [
    # "basic prompt multilabel",
    # "gpt prompt multilabel unranked",
    # "basic prompt generation",
    # "carina trial generation",
    # "carina trial multilabel unranked",
    # "carina trial multilabel unranked one option"

    ##optional##### "basic prompt multilabel ranked_3.5_4096",
    ##optional##### "explanation prompt multilabel ranked_3.5_4096",

    ###------------------

    "basic_prompt_multilabel_no_constrictions_unranked",
    "basic_prompt_generation_up_to_2",
    "explanation_prompt_generation_up_to_2",
    "explanation_prompt_multilabel_unranked_up_to_2",
    "example_prompt_multilabel_unranked_up_to_2",
    "example_prompt_generation_up_to_2",
    "basic_prompt_multilabel_unranked_up_to_2",
    "basic_prompt_generation_no_constrictions",
    "auto_prompt_output",
    "basic_prompt_single_label"
]


def create_requests_file_for_experiment(prompt_initial, experiment_name):
    csv_file_path = 'data after manipulation/final_all.csv'
    jsonl_file_path = 'requests_jsonl/' + experiment_name + '_requests.jsonl'

    # Open the CSV file for reading
    with open(csv_file_path, mode='r', newline='', encoding='ISO-8859-1') as csvfile:
        # Read the CSV file
        csvreader = csv.DictReader(csvfile)

        # Open the JSONL file for writing
        with open(jsonl_file_path, mode='w', encoding='utf-8') as jsonlfile:
            # Iterate over each row in the CSV
            request_num = 1
            for row in csvreader:
                # Get the value from the 'Description' column
                description = row.get('Description', '')
                whole_prompt = prompt_initial + description
                # Prepare the content string
                jsonl_entry = {'custom_id': 'request-' + str(request_num), 'method': 'POST',
                               'url': '/v1/chat/completions', 'body': {'model': 'gpt-4o-mini', 'messages': [
                        {'role': 'system',
                         'content': 'You are a cybersecurity expert specializing in identifying network protocols related to vulnerabilities.'},
                        {'role': 'user', 'content': whole_prompt}], 'max_tokens': 25}}
                # Write the dictionary as a JSON object in the JSONL file
                jsonlfile.write(json.dumps(jsonl_entry) + '\n')
                request_num += 1


def run_experiments():
    # df = pd.read_csv('data after manipulation/all_samples.csv')
    # df = df.head(30)
    for i in range(len(prompt_experiments)):
        create_requests_file_for_experiment(prompt_experiments[i], experiment_names[i])
        # updated_df.to_csv(experiment_names[i]+'.csv', index=False)


run_experiments()
