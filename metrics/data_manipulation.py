import pandas as pd
import numpy as np
protocols = ['DNS', 'DHCP', 'ICMP', 'BGP', 'SMTP', 'POP3', 'SSH', 'ARP', 'FTP', 'SSL']


def create_tables_per_protocol():
    protocols = df['Protocol'].unique()
    print(df.iloc[13]['Protocol'])
    for protocol in protocols:
        protocol_df = df[df['Protocol'] == protocol]
        protocol_df.to_csv(f'{protocol}_table.csv', index=False)


def equal_tables():
    original_df = pd.read_csv('all.csv')
    original_df['Protocol'] = original_df['Protocol'].fillna('None')
    protocol_files = ['ARP_table.csv', 'BGP_table.csv', 'ICMP_table.csv', 'None_table.csv', 'POP3_table.csv',
                      'Both_table.csv', 'DHCP_table.csv', 'DNS_table.csv', 'FTP_table.csv', 'SMTP_table.csv',
                      'SSL_table.csv', 'SSH_table.csv']  # Add all protocol files here

    protocol_dfs = [pd.read_csv(file) for file in protocol_files]
    combined_df = pd.concat(protocol_dfs, ignore_index=True)

    original_df_sorted = original_df.sort_values(by=original_df.columns.tolist()).reset_index(drop=True)
    combined_df_sorted = combined_df.sort_values(by=combined_df.columns.tolist()).reset_index(drop=True)

    if original_df_sorted.equals(combined_df_sorted):
        print("All rows are accounted for. The union of protocol tables matches the original table.")
    else:
        print("Mismatch found. The union of protocol tables does NOT match the original table.")


def create_hard_samples():
    # df = pd.read_csv('all.csv')
    # filtered_df = df[~df.apply(lambda row: str(row['Protocol']) in str(row['Description']), axis=1)]
    filtered_df = df[~df.apply(lambda row: str(row['Protocol']).lower() in str(row['Description']).lower(), axis=1)]
    filtered_df = filtered_df[filtered_df['Protocol'] != 'None']
    filtered_df = filtered_df[filtered_df['Protocol'] != 'Both']
    filtered_df.to_csv('new_description_does_not_have_protocol.csv', index=False)


def create_one_protocol_samples():
    filtered_df = df[(df['Protocol'] != 'None') & (df['Protocol'] != 'Both')]
    filtered_df.to_csv('one_protocol_samples.csv', index=False)


def contains_other_protocol(row):
    current_protocol = str(row['Protocol']).lower()
    for protocol in protocols:
        protocol_str = str(protocol).lower()  # Ensure case-insensitive check
        if protocol_str != current_protocol and protocol_str in str(row['Description']).lower():
            return True
    return False


def create_has_other_protocol_in_description():
    filtered_df = df[df.apply(contains_other_protocol, axis=1)]
    filtered_df.to_csv('new_has_other_protocol_in_description.csv', index=False)


def create_n_samples_for_autoprompt():
    protocol_counts = df['Protocol'].value_counts(normalize=True)

    sampled_df = pd.DataFrame()

    for protocol, proportion in protocol_counts.items():
        n_samples = int(np.round(proportion * 30))

        sampled_protocol = df[df['Protocol'] == protocol].sample(n_samples, random_state=42)

        sampled_df = pd.concat([sampled_df, sampled_protocol])

    sampled_df = sampled_df.sample(frac=1, random_state=42).reset_index(drop=True)

    sampled_df.to_csv('new_sampled_table.csv', index=False)


def check_unique_cve_id(df):
    if df['CVE-ID'].is_unique:
        return True
    else:
        non_unique_values = df['CVE-ID'][df['CVE-ID'].duplicated()]
        print("Non-unique values found:", non_unique_values.unique())
        print("count:", len(non_unique_values.unique()))


def cancel_duplicates(df):
    df_unique = df.drop_duplicates()

    df_unique.to_csv("no_duplicates_and_same_tag.csv", index=False)


def group_by_cve_id(df):
    id_counts = df['CVE-ID'].value_counts()

    duplicate_rows = df[df['CVE-ID'].isin(id_counts[id_counts > 1].index)]
    unique_rows = df[df['CVE-ID'].isin(id_counts[id_counts == 1].index)]

    duplicate_rows = duplicate_rows.sort_values(by='CVE-ID')

    sorted_df = pd.concat([duplicate_rows, unique_rows])

    sorted_df.to_csv('no_duplicated_and_same_tag_sorted_carina_manual.csv', index=False)


def count_unique_cve_ids(df):
    unique_count = df['CVE-ID'].nunique()
    return unique_count


# df = pd.read_csv('all.csv')
df = pd.read_csv('data after manipulation/final_all.csv', encoding='ISO-8859-1')
df['Protocol'] = df['Protocol'].fillna('None')
# protocols = df['Protocol'].unique()



