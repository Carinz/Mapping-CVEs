import asyncio
import time

import openai
import pandas as pd

openai.api_key = ''

prompt_experiments = [
    # In your answer only state your final protocol or protocols
    # "What are the protocols of the following CVE? Choose which ones you think apply from these protocols: 'DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL' or None. In your answer mention the protocol or protocols first. This is the CVE's description: ",
    # "Please analyze [CVE number] and determine which of the following protocols: DNS, DHCP, ICMP, BGP, SMTP, POP3, SSH, ARP, FTP, SSL or None, are relevant to it. Provide a detailed explanation for your choices, including why each selected protocol is applicable. In your response state first your final answer for the protocol or protocols then the rest of your answer. This is the CVE's description: "
    # "What protocol or protocols is this CVE about? For any protocol you mention, state your confidence in it. In your response state first your final answer for the protocol or protocols then the rest of your answer. This is the CVE's description: "
    # "Tag for the given CVE which protocol the weakness of it is about. The CVE number is [CVE number] and the CVE's description is: "
    # "What are the protocols of the following CVE? Choose which ones you think apply from these protocols: 'DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL' or None. The CVE's number is [CVE number] and this is the CVE's description: "
    # "What is the protocol of the following CVE? Choose which one you think apply best from these protocols: 'DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL' or None. Explain your answer. In your response state first your final answer for the protocol or protocols then the rest of your answer. The CVE's number is [CVE number] and this is the CVE's description: "
    # "The following CVE describes a vulnerability in one of these protocols: 'DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL', or none. Or, in two of these protocols, but less likely. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) or 'none'. Here is the CVE description: "
    ###------------------

    # "The following CVE describes a vulnerability in one or more of these protocols: 'DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL', or none. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) or 'none'. Here is the CVE description: "
    ###optional##### "The following CVE describes a vulnerability in one or more of these protocols: 'DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL', or none. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) or 'none'. Additionally, rank these protocols and state your confidence level regarding the likelihood that the CVE pertains to them. Here is the CVE description: ",
    "The following CVE describes a vulnerability in one or two protocols, or possibly none. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) or 'none'. Here is the CVE description: ",
    # "The following CVE describes a vulnerability in one or two protocols, or possibly none. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) or 'none', then explain your answer. Here is the CVE description: "
    ###optional#####  "The following CVE describes a vulnerability in one or more of these protocols: 'DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL', or none. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) or 'none' then explain your answer. Additionally, rank these protocols and state your confidence level regarding the likelihood that the CVE pertains to them. Here is the CVE description: "
    # "The following CVE describes a vulnerability in one or two of these protocols: 'DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL', or none. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) or 'none' then explain your answer. Here is the CVE description: "
    # "The following CVE describes a vulnerability in one or two of these protocols: 'DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL', or none. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) or 'none'. For example, in this CVE description the answer is none: 'IBM Jazz Foundation (IBM Rational Collaborative Lifecycle Management 5.0 through 6.0.6) is vulnerable to HTTP header injection, caused by improper validation of input. By persuading a victim to visit a specially-crafted Web page, a remote attacker could exploit this vulnerability to inject arbitrary HTTP headers, which will allow the attacker to conduct various attacks against the vulnerable system, including cross-site scripting, cache poisoning or session hijacking. IBM X-Force ID: 144884.'. In this CVE description the answer is 'DNS': 'The Microsoft Windows Domain Name System (DNS) DNSAPI.dll on Microsoft Windows 8.1, Windows Server 2012 R2, Windows RT 8.1, Windows 10 Gold, 1511, 1607, and 1703, and Windows Server 2016 allows a remote code execution vulnerability when it fails to properly handle DNS responses, aka 'Windows DNSAPI Remote Code Execution Vulnerability'. Here is the CVE description you need to answer: "
    # "The following CVE describes a vulnerability in one or two protocols, or possibly none. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) or 'none'. For example, in this CVE description the answer is none: 'IBM Jazz Foundation (IBM Rational Collaborative Lifecycle Management 5.0 through 6.0.6) is vulnerable to HTTP header injection, caused by improper validation of input. By persuading a victim to visit a specially-crafted Web page, a remote attacker could exploit this vulnerability to inject arbitrary HTTP headers, which will allow the attacker to conduct various attacks against the vulnerable system, including cross-site scripting, cache poisoning or session hijacking. IBM X-Force ID: 144884.'. In this CVE description the answer is 'DNS': 'The Microsoft Windows Domain Name System (DNS) DNSAPI.dll on Microsoft Windows 8.1, Windows Server 2012 R2, Windows RT 8.1, Windows 10 Gold, 1511, 1607, and 1703, and Windows Server 2016 allows a remote code execution vulnerability when it fails to properly handle DNS responses, aka 'Windows DNSAPI Remote Code Execution Vulnerability'. Here is the CVE description you need to answer: ",
    # "The following CVE describes a vulnerability in one or two of these protocols: 'DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL', or none. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) or 'none'. Here is the CVE description: "
]

experiment_names = [
    # "basic prompt multilabel",
    # "gpt prompt multilabel unranked",
    # "basic prompt generation",
    # "carina trial generation",
    # "carina trial multilabel unranked",
    # "carina trial multilabel unranked one option"
    # "carina attempt to narrow"
    ###------------------

    # "basic_prompt_multilabel_no_constrictions_unranked",
    ##optional##### "basic prompt multilabel ranked_3.5_4096",
    "basic_prompt_generation_up_to_2"
    # "explanation_prompt_up_to_2_generation",
    ##optional##### "explanation prompt multilabel ranked_3.5_4096",
    # "explanation prompt multilabel up to 2 unranked_3.5_4096",
    # "example prompt multilabel unranked up to 2_3.5_4096",
    # "example prompt generation up to 2_3.5_4096",
    # "basic_prompt_multilabel_up_to_2_unranked",
]


def get_chatgpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            # model="gpt-3.5-turbo",  # or use "gpt-3.5-turbo"
            model="gpt-4o-mini",  # or use "gpt-3.5-turbo"
            messages=[{"role": "system",
                       "content": "You are a cybersecurity expert specializing in identifying network protocols related to vulnerabilities."},
                      {"role": "user", "content": prompt}],  # This is how the chat format works
            # max_tokens=4096  # Adjust this based on how long you want the response
            max_tokens=15  # Adjust this based on how long you want the response
            # max_tokens = 150  # Adjust this based on how long you want the response
        )

        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        return f"An error occurred: {str(e)}"


def get_responses(df, prompt, experiment_name):
    responses = []  # List to store responses
    # prompts = []

    for index, row in df.iterrows():
        description = row['Description']
        CVE_ID = row['CVE-ID']
        # if  experiment_name == "carina trial multilabel unranked one option" or experiment_name == "gpt prompt multilabel unranked" or experiment_name == "carina trial generation" or experiment_name == "carina trial multilabel unranked":
        if "[CVE number]" in prompt:
            prompt = prompt.replace("[CVE number]", CVE_ID)
        # prompt = "What are the protocols of the following CVE? Choose which ones you think apply from these protocols: 'DNS', 'DHCP', 'Both', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL' or None. This is the CVE's description:" + description
        prompt += description
        # prompts+=prompt
        response = get_chatgpt_response(prompt)
        # while "An error occurred" in response:
        #     time.sleep(0.1)
        #     response = get_chatgpt_response(prompt)

        responses.append(response)

    df['ChatGPT_Response'] = responses
    # return prompts
    return df


def run_experiments():
    # df = pd.read_csv('data after manipulation/all_samples.csv', encoding= 'ISO-8859-1')
    df = pd.read_csv('data after manipulation/None_table.csv', encoding='ISO-8859-1')
    # df = df.head(5)
    for i in range(len(prompt_experiments)):
        updated_df = get_responses(df, prompt_experiments[i], experiment_names[i])
        updated_df.to_csv("serial_experiments/" + experiment_names[i] + '.csv', index=False)


if __name__ == "__main__":
    # user_prompt = "What are the protocols of the following CVE? Choose which ones you think apply from these protocols: 'DNS', 'DHCP', 'Both', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL' or None. This is the CVE's description: The Loving - Couple Essential (aka com.xiaoenai.app) application 4.0.1 for Android does not verify X.509 certificates from SSL servers, which allows man-in-the-middle attackers to spoof servers and obtain sensitive information via a crafted certificate."
    # user_prompt = "What are the protocols of the following CVE? Choose which ones you think apply from these protocols: 'DNS', 'DHCP', 'Both', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL' or None. This is the CVE's description: IBM Jazz Foundation (IBM Rational Collaborative Lifecycle Management 5.0 through 6.0.6) is vulnerable to HTTP header injection, caused by improper validation of input. By persuading a victim to visit a specially-crafted Web page, a remote attacker could exploit this vulnerability to inject arbitrary HTTP headers, which will allow the attacker to conduct various attacks against the vulnerable system, including cross-site scripting, cache poisoning or session hijacking. IBM X-Force ID: 144884."
    # chatgpt_response = get_chatgpt_response(user_prompt)
    # print("ChatGPT Response:", chatgpt_response)
    # df = df.head(25)

    run_experiments()
