import numpy as np
import shutil


# Function to extract from model output a string of protocols of the same format as GT
def extract_protocols_from_prediction(prediction, protocol_list):
    # Initialize an empty set to store found protocols
    found_protocols = set()

    # Check for each protocol in the prediction string
    for protocol in protocol_list:
        if protocol in prediction:
            found_protocols.add(protocol)

    # Join the found protocols into a comma-separated string
    return ', '.join(sorted(found_protocols))


# Function to calculate accuracy
def accuracy_score_per_sample(gt, prediction):
    if not gt and not prediction:  # Handle cases where both are empty strings
        return 1.0

    # Split the strings by ', ' and convert them to sets
    gt_set = set(gt.split(', ')) if gt else set()
    prediction_set = set(prediction.split(', ')) if prediction else set()

    intersection = gt_set.intersection(prediction_set)  # True positives
    union = gt_set.union(prediction_set)  # All unique protocols (gt + predicted)

    return len(intersection) / len(union) if len(union) > 0 else 0.0


# Function to calculate Precision@k
def precision_at_k(gt, prediction, k=5):
    # Convert strings to lists of protocols
    gt = gt.split(', ')
    prediction = prediction.split(', ')

    if len(prediction) > k:
        prediction = prediction[:k]

    correct = sum([1 for protocol in prediction if protocol in gt])
    return correct / len(prediction) if len(prediction) > 0 else 0.0


# Function to calculate Reciprocal Rank (RR) for one sample
def reciprocal_rank(gt, prediction):
    gt = gt.split(', ')
    prediction = prediction.split(', ')

    for rank, protocol in enumerate(prediction, start=1):
        if protocol in gt:
            return 1 / rank
    return 0.0  # Return 0 if none of the true protocols are found


# Function to evaluate a pandas DataFrame
def evaluate_predictions(df, protocol_list, k=5):
    accuracies = []
    p_at_k_scores = []
    mrr_scores = []

    # Iterate through each row in the DataFrame
    for idx, row in df.iterrows():
        gt = row['gt']  # Ground truth protocols
        prediction = extract_protocols_from_prediction(row['prediction'], protocol_list)  # Model predictions

        # Compute Accuracy
        acc = accuracy_score_per_sample(gt, prediction)
        accuracies.append(acc)

        # Compute Precision@k
        p_at_k = precision_at_k(gt, prediction, k)
        p_at_k_scores.append(p_at_k)

        # Compute MRR
        mrr = reciprocal_rank(gt, prediction)
        mrr_scores.append(mrr)

    # Return the mean scores across the dataset
    return {
        'accuracy': np.mean(accuracies),
        'precision@k': np.mean(p_at_k_scores),
        'mrr': np.mean(mrr_scores)
    }


# Function to replace YAML config
def replace_yaml_config(source_file, destination_file):
    try:
        # Replace the YAML file at the destination with the source file
        shutil.copy(source_file, destination_file)
        print(f"Successfully replaced config with {source_file}")
    except Exception as e:
        print(f"Error replacing config: {e}")


# Function to set AutoPrompt config
def set_autoprompt_config(predictor_type, max_num_labels):
    """
    :param predictor_type: 'local' or 'gpt'.
    :param max_num_labels: 1 or 2.
    """
    source_file = f'config/config_default_{predictor_type}_{max_num_labels}.yml'
    destination_file = 'config/config_default.yml'  # Path to the target config
    replace_yaml_config(source_file, destination_file)


# # Example usage:
# # Assume df has 'gt' and 'prediction' columns, where each entry is a string
# df = pd.DataFrame({
#     'gt': ['POP3, TCP', 'SSH', 'FTP', ''],
#     'prediction': ['i like POP3, and FTP', 'all SSH are beautiful', 'FTP? more like FTW', 'ARP is a cat']
# })
#
# # List of all possible protocols
# protocol_list = ['ARP', 'BGP', 'ICMP', 'POP3', 'DHCP', 'DNS', 'FTP', 'SMTP', 'SSL', 'SSH', 'none']
#
# # Evaluate predictions
# metrics = evaluate_predictions(df, protocol_list, k=3)
# print(metrics)
# set_autoprompt_config(predictor_type='local', max_num_labels=2)

