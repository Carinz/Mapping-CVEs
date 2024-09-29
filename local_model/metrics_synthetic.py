import pandas as pd

protocols = ['DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL']

file_names = {
    "calibrated_prompt_up_to_1_none": "model_responses_synthetic/calibrated_prompt_up_to_1_none.csv",
    "calibrated_prompt_up_to_1_single": "model_responses_synthetic/calibrated_prompt_up_to_1_single.csv",
    "initial_prompt_up_to_1_none": "model_responses_synthetic/initial_prompt_up_to_1_none.csv",
    "initial_prompt_up_to_1_single": "model_responses_synthetic/initial_prompt_up_to_1_single.csv"
}

for f in file_names:

    # Input CSV file path
    input_csv_file = file_names[f]

    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv_file)

    # Replace NaN or empty values with "none" in both 'Protocol' and 'Model_Response' columns
    df['Protocol'] = df['Protocol'].fillna('none').replace('', 'none')
    df['Model_Response'] = df['Model_Response'].fillna('none').replace('', 'none')

    # Strip spaces and convert to lowercase in both columns
    df['Protocol'] = df['Protocol'].str.strip().str.lower()
    df['Model_Response'] = df['Model_Response'].str.strip().str.lower()

    # Calculate the mean where 'Protocol' == 'Model_Response'
    mean_value = (df['Protocol'] == df['Model_Response']).mean()

    # Print the result
    print(f"The mean of accuracy for {f} is: {mean_value}")
