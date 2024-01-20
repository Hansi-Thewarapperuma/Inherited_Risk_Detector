'''
Function: Evaluation through minor allele frequency criterion
Input: Dataframe
Output: A list of tuples containing index and evaluation (rare, common, N/A)

Author: Hansi Thewarapperuma
date: 12/12/2023
'''

import pandas as pd

def evaluate_minor_allele_freq(input_variants_df):
    # generating allele frequency subset dataframe (allele_freq_df) from the original dataframe (input_variants_df)
    allele_freq_df = input_variants_df.loc[:, ['non_cancer_AF', 'non_neuro_AF', 'controls_AF', 'non_topmed_AF',
                                               'AF_sas', 'AF_amr', 'AF_nfe', 'AF_eas', 'AF_afr',
                                               'AF_nfe_onf', 'AF_eas_oea', 'AF_nfe_nwe', 'AF_nfe_seu', 'AF_nfe_swe',
                                               'AF_eas_jpn', 'AF_eas_kor', 'AF_fin', 'AF_asj', 'AF_nfe_est', 'AF_oth']]

    results = []

    # Iterate through each row of the dataframe
    for index, row in allele_freq_df.iterrows():
        # Check if all the mentioned columns have 'N/A' values
        all_na = all(pd.isna(row[col]) or str(row[col]) == 'N/A' for col in
                     ['non_cancer_AF', 'non_neuro_AF', 'controls_AF', 'non_topmed_AF',
                      'AF_sas', 'AF_amr', 'AF_nfe', 'AF_eas', 'AF_afr',
                      'AF_nfe_onf', 'AF_eas_oea', 'AF_nfe_nwe', 'AF_nfe_seu', 'AF_nfe_swe',
                      'AF_eas_jpn', 'AF_eas_kor', 'AF_fin', 'AF_asj', 'AF_nfe_est', 'AF_oth'])
        if not all_na:  # At least one non-'N/A' value in the mentioned columns
            # Convert non-missing values to numerics
            numeric_values = [pd.to_numeric(value, errors='coerce') for value in row]

            #*********** IMPLEMENTATION OF SIMPLE ENSEMBLE LEARNING METHOD USING AVERAGE ***********

            # Count occurrences of unique values for the row
            value_counts = pd.Series(numeric_values).value_counts()

            # Calculate the sum of (value * count) for each unique value
            weighted_sum = sum(value * count for value, count in value_counts.items())

            # Calculate the total count of occurrences
            total_count = value_counts.sum()

            # Ensure total_count is not zero before dividing, since division by zero is not defined
            if total_count != 0:
                # Calculate the average by dividing the weighted sum by the total count
                average_value = weighted_sum / total_count

            # Determine evaluation based on average value
            if average_value < 0.01:
                results.append((index, 'rare'))
            elif average_value > 0.01:
                results.append((index, 'common'))
            else:
                results.append((index, 'N/A'))
        else:
            results.append((index, 'N/A'))

    # Returning a list of tuples containing the index and the evaluation for each row in the DataFrame
    return results
