import csv
import re

import pandas as pd
import numpy as np

local_type = "Local"
GPT_type = "GPT"

protocols = ['DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL']

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

experiment_names_on_local = [

    "basic_prompt_multilabel_no_constrictions_unranked",
    "basic_prompt_generation_up_to_2",
    "explanation_prompt_generation_up_to_2",
    "explanation_prompt_multilabel_unranked_up_to_2",
    "example_prompt_multilabel_unranked_up_to_2",
    "example_prompt_generation_up_to_2",
    "basic_prompt_multilabel_unranked_up_to_2",
    "basic_prompt_generation_no_constrictions",

    "calibrated_prompt_up_to_1",
    "calibrated_prompt_up_to_2",
    "basic_prompt_single_label"
]


def calculate_f1(precision, recall):
    if precision + recall == 0:
        return 0
    return 2 * (precision * recall) / (precision + recall)


def create_df_per_protocol(df):
    dfs = []
    for protocol in protocols:
        protocol_df = df[df['Protocol'] == protocol]
        dfs.append(protocol_df)
    return dfs


def create_table_one_protocol(df):
    filtered_df = df[~df['Protocol'].str.contains(',', na=False)]
    return filtered_df


def create_table_two_protocols(df):
    filtered_df = df[df['Protocol'].str.contains(',', na=False)]
    return filtered_df


def replace_first_newline_with_space(text):
    if "\n" in text:
        return text.replace("\n", " ")  # Replace only the first occurrence
    return text  # Return the original text if no "\n" is found


def truncate_after_th(text):
    return re.split(r'[tT]h', text, maxsplit=1)[0]


def sanitize_explanation_response(model_type):
    if model_type == GPT_type:
        model_type = "batch"
        response_column_name = 'ChatGPT_Response'
    else:
        model_type = "local"
        response_column_name = 'Model_Response'

    df_explanation_generation = pd.read_csv(
        model_type + '_experiments/' + "explanation_prompt_generation_up_to_2" + '.csv', encoding='ISO-8859-1')
    df_explanation = pd.read_csv(
        model_type + '_experiments/' + "explanation_prompt_multilabel_unranked_up_to_2" + '.csv', encoding='ISO-8859-1')

    df_explanation_generation[response_column_name] = df_explanation_generation[response_column_name].apply(
        replace_first_newline_with_space)
    df_explanation[response_column_name] = df_explanation[response_column_name].apply(replace_first_newline_with_space)

    df_explanation_generation[response_column_name] = df_explanation_generation[response_column_name].apply(
        truncate_after_th)
    df_explanation[response_column_name] = df_explanation[response_column_name].apply(truncate_after_th)

    df_explanation_generation[response_column_name] = df_explanation_generation[response_column_name].str.replace(
        'because', '', regex=False)
    df_explanation[response_column_name] = df_explanation[response_column_name].str.replace('because', '', regex=False)

    df_explanation_generation[response_column_name] = df_explanation_generation[response_column_name].str.replace(
        'Explanation', '', regex=False)
    df_explanation[response_column_name] = df_explanation[response_column_name].str.replace('Explanation', '',
                                                                                            regex=False)

    df_explanation_generation.to_csv(model_type + '_experiments/' + "explanation_prompt_generation_up_to_2" + '.csv',
                                     index=False)
    df_explanation.to_csv(model_type + '_experiments/' + "explanation_prompt_multilabel_unranked_up_to_2" + '.csv',
                          index=False)


def sanitize_auto_prompt_response(model_type):
    if model_type == GPT_type:
        model_type = "batch"

        # TODO: UNCOMMENT
        df = pd.read_csv(model_type + '_experiments/' + "auto_prompt_output" + '.csv', encoding='ISO-8859-1')
        df['Protocol'] = df['Protocol'].fillna('None')
        df_sanitize = create_table_one_protocol(df)
        df_sanitize.to_csv(model_type + '_experiments/' + "auto_prompt_output" + '.csv', index=False)

        df = pd.read_csv(model_type + '_experiments/' + "basic_prompt_single_label" + '.csv', encoding='ISO-8859-1')
        df['Protocol'] = df['Protocol'].fillna('None')
        df_sanitize = create_table_one_protocol(df)
        df_sanitize.to_csv(model_type + '_experiments/' + "basic_prompt_single_label" + '.csv', index=False)

    else:
        model_type = "local"

        df = pd.read_csv(model_type + '_experiments/' + "calibrated_prompt_up_to_1" + '.csv', encoding='ISO-8859-1')
        df['Protocol'] = df['Protocol'].fillna('None')
        df_sanitize = create_table_one_protocol(df)
        df_sanitize.to_csv(model_type + '_experiments/' + "calibrated_prompt_up_to_1" + '.csv', index=False)

        df = pd.read_csv(model_type + '_experiments/' + "basic_prompt_single_label" + '.csv', encoding='ISO-8859-1')
        df['Protocol'] = df['Protocol'].fillna('None')
        df_sanitize = create_table_one_protocol(df)
        df_sanitize.to_csv(model_type + '_experiments/' + "basic_prompt_single_label" + '.csv', index=False)


def count_unique_words(input_string, reference_words):
    words = [word.strip() for word in input_string.split(',') if word.strip()]

    counted_words = set()

    for word in words:
        for ref_word in reference_words:
            if ref_word.lower() in word.lower():  # Case-insensitive comparison
                counted_words.add(ref_word.lower())
                break
        else:
            counted_words.add(word.lower())

    return len(counted_words)


def calculate_jaccard(ground_truth, prediction):
    protocols = ['DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL']
    # private case
    if ground_truth == "None" and prediction not in protocols:
        return 1

    ground_truth = ground_truth.lower()
    prediction = prediction.lower()

    ground_truth_set = set([protocol.strip() for protocol in ground_truth.split(',')])
    intersection_predicted_set = set()
    num_predicted_protocols = count_unique_words(prediction, protocols)
    for predicted_word in prediction.split(','):
        predicted_word = predicted_word.strip()
        for protocol in ground_truth_set:
            if protocol in predicted_word:
                intersection_predicted_set.add(protocol)

    # intersection = ground_truth_set.intersection(predicted_set)
    # union = ground_truth_set.union(predicted_set)
    union_len = num_predicted_protocols + len(ground_truth_set) - len(intersection_predicted_set)
    if union_len == 0:
        return 0
    return len(intersection_predicted_set) / union_len


def calculate_precision(ground_truth, prediction):
    protocols = ['DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL']
    # private case
    if ground_truth == "None" and prediction not in protocols:
        return 1

    ground_truth = ground_truth.lower()
    prediction = prediction.lower()

    ground_truth_set = set([protocol.strip() for protocol in ground_truth.split(',')])
    intersection_predicted_set = set()
    num_predicted_protocols = count_unique_words(prediction, protocols)
    for predicted_word in prediction.split(','):
        predicted_word = predicted_word.strip()
        for protocol in ground_truth_set:
            if protocol in predicted_word:
                intersection_predicted_set.add(protocol)

    # intersection = ground_truth_set.intersection(predicted_set)
    # union = ground_truth_set.union(predicted_set)
    # union_len = num_predicted_protocols + len(ground_truth_set) - len(intersection_predicted_set)
    # if union_len == 0:
    #     return 0
    return len(intersection_predicted_set) / num_predicted_protocols


def calculate_recall(ground_truth, prediction):
    protocols = ['DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL']
    # private case
    if ground_truth == "None" and prediction not in protocols:
        return 1

    ground_truth = ground_truth.lower()
    prediction = prediction.lower()

    ground_truth_set = set([protocol.strip() for protocol in ground_truth.split(',')])
    intersection_predicted_set = set()
    num_predicted_protocols = count_unique_words(prediction, protocols)
    for predicted_word in prediction.split(','):
        predicted_word = predicted_word.strip()
        for protocol in ground_truth_set:
            if protocol in predicted_word:
                intersection_predicted_set.add(protocol)

    # intersection = ground_truth_set.intersection(predicted_set)
    # union = ground_truth_set.union(predicted_set)
    # union_len = num_predicted_protocols + len(ground_truth_set) - len(intersection_predicted_set)
    # if union_len == 0:
    #     return 0
    return len(intersection_predicted_set) / len(ground_truth_set)


def calc_metrics_for_experiments(model_type, experiment_names_lst):
    if model_type == GPT_type:
        model_type_experiment = "batch"
        response_column_name = 'ChatGPT_Response'
    else:
        model_type_experiment = "local"
        response_column_name = 'Model_Response'

    for file_name in experiment_names_lst:
        df = pd.read_csv(model_type_experiment + '_experiments/' + file_name + '.csv', encoding='ISO-8859-1')
        df['Protocol'] = df['Protocol'].fillna('None')
        df[response_column_name] = df[response_column_name].fillna('None')
        df['Jaccard_Score'] = df.apply(lambda row: calculate_jaccard(row['Protocol'], row[response_column_name]),
                                       axis=1)
        df['Precision_Score'] = df.apply(lambda row: calculate_precision(row['Protocol'], row[response_column_name]),
                                         axis=1)
        df['Recall_Score'] = df.apply(lambda row: calculate_recall(row['Protocol'], row[response_column_name]), axis=1)
        df.to_csv('metrics_results/' + model_type + '/' + file_name + '_with_metrics.csv', index=False)


def add_f1_score(model_type, experiment_names_lst):
    for file_name in experiment_names_lst:
        df = pd.read_csv('metrics_results/' + model_type + '/' + file_name + '_with_metrics.csv', encoding='ISO-8859-1')
        df['F1_Score'] = df.apply(lambda row: calculate_f1(row['Precision_Score'], row['Recall_Score']), axis=1)
        df.to_csv('metrics_results/' + model_type + '/' + file_name + '_with_metrics.csv', index=False)


def calc_mean_metrics(df, table_type, experiment_name, model_type):
    summary_df = pd.DataFrame({
        'Metric': ['Table Type', 'Mean Jaccard', 'Mean Precision', 'Mean Recall', 'Mean F1', 'Number Samples'],
        'Value': [table_type, df["Jaccard_Score"].mean(), df["Precision_Score"].mean(), df["Recall_Score"].mean(),
                  df["F1_Score"].mean(), df.shape[0]]
    })
    summary_df.to_csv(
        'metrics_results/' + model_type + '/mean_metrics/' + experiment_name + '/' + 'mean_' + table_type + '.csv',
        index=False)


def calc_all_mean_metrics(model_type, experiment_names_lst):
    for experiment_name in experiment_names_lst:
        df = pd.read_csv('metrics_results/' + model_type + '/' + experiment_name + '_with_metrics.csv',
                         encoding='ISO-8859-1')
        calc_mean_metrics(df, "all", experiment_name, model_type)

        protocol_dfs = create_df_per_protocol(df)
        for i in range(len(protocol_dfs)):
            calc_mean_metrics(protocol_dfs[i], protocols[i], experiment_name, model_type)
        calc_mean_metrics(create_table_one_protocol(df), "1_protocol", experiment_name, model_type)
        calc_mean_metrics(create_table_two_protocols(df), "2_protocol", experiment_name, model_type)


def metric_all_experiments_together(type_table_comparison, model_type, experiment_names_lst):
    df_first_column = pd.read_csv('metrics_results/' + model_type + '/mean_metrics/' + experiment_names_lst[
        0] + '/mean_' + type_table_comparison + '.csv')[["Metric"]]
    final_df = df_first_column.copy()
    for experiment_name in experiment_names_lst:
        df = pd.read_csv(
            'metrics_results/' + model_type + '/mean_metrics/' + experiment_name + '/mean_' + type_table_comparison + '.csv',
            encoding='ISO-8859-1')
        df = df[['Value']].rename(columns={'Value': experiment_name})
        final_df = pd.concat([final_df, df], axis=1)
    final_df.rename(columns={'Metric': 'Experiment'}, inplace=True)
    column_names = final_df.columns
    final_df.iloc[0] = column_names
    final_df = final_df.transpose()
    final_df_sorted = final_df.sort_values(by=1, ascending=False)  # Jaccard
    final_df_sorted.to_csv(
        'metrics_results/' + model_type + '/mean_metrics/experiments_comparison_metrics_' + type_table_comparison + '.csv',
        index=False)


def calc_metrics_per_model(model_type, experiment_names_lst):
    sanitize_explanation_response(model_type)
    sanitize_auto_prompt_response(model_type)
    calc_metrics_for_experiments(model_type, experiment_names_lst)
    add_f1_score(model_type, experiment_names_lst)
    calc_all_mean_metrics(model_type, experiment_names_lst)
    metric_all_experiments_together("all", model_type, experiment_names_lst)
    metric_all_experiments_together("1_protocol", model_type, experiment_names_lst)


calc_metrics_per_model(local_type, experiment_names_on_local)
calc_metrics_per_model(GPT_type, experiment_names)
