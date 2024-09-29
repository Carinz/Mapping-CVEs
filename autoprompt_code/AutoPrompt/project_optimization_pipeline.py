import project_utils
import subprocess

# Choose 'local' or 'gpt'
predictor_type = 'gpt'

# For each maximal number of GT protocols in dataset (at most 1 or at most 2)
for max_num_labels in [1, 2]:
    # Define initial prompt
    initial_prompt = "The following CVE describes a vulnerability in one of these protocols: 'DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL', or none. Which protocol is it? If none, please specify 'none'. In your answer the only word should be the protocol or 'none'." \
            if max_num_labels == 1 \
            else "The following CVE describes a vulnerability in one or two of these protocols: 'DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL', or none. Which protocol(s) is it? If none, please specify 'none'. In your answer the first word(s) should be the protocol(s) (separated by commas for more than one protocol) or 'none'."
    # For each score function: standard accuracy and union accuracy (which takes into account partial overlap)
        # Set AutoPrompt config to current setup
    project_utils.set_autoprompt_config(predictor_type=predictor_type,
                                max_num_labels=max_num_labels)

    # Define the command to run
    command = [
        "python", "run_pipeline.py",
        "--prompt", initial_prompt,
        "--task_description",
        "You are a cybersecurity expert specializing in identifying network protocols related to vulnerabilities.",
        # "--num_steps", "30"   # Don't specify number of steps
    ]

    # Run the command
    subprocess.run(command, shell=True, check=True)
