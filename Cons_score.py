'''
Function: Evaluation through conservation scores criterion
Input: Dataframe
Ouput: A list of tuples containing index and evaluation (conserved, not_conserved, N/A)

Author: Hansi Thewarapperuma
date: 13/12/2023
'''

import pandas as pd

def conservation_scores(input_variants_df):

    # Define relevant columns
    phyloP100_column = 'dbNSFP_phyloP100way_vertebrate'
    phastCons_column = 'dbNSFP_phastCons100way_vertebrate'
    phyloP30_column = 'dbNSFP_phyloP30way_mammalian'

    gerp_column = "dbNSFP_GERP___RS"
    eigen_column = "dbNSFP_Eigen_raw_coding"

    # Convert specified columns to numeric, handling non-numeric values
    numeric_columns = [phyloP100_column, phastCons_column, phyloP30_column, gerp_column, eigen_column]
    input_variants_df[numeric_columns] = input_variants_df[numeric_columns].apply(pd.to_numeric, errors='coerce')

    # initialize an empty list to save results (index: conservation status)
    results = []

    # iterate through each row of the dataframe
    for index, row in input_variants_df.iterrows():
        # Check for N/A values and get the total count
        na_count = row[numeric_columns].isna().sum()

        # If all the column values are not N/A (for the rows with values mixed with NA too)
        if na_count < len(numeric_columns):  # If there is at least one non-N/A value

            # The conservation thresholds for each in-silco tool to confirm the conservation status
            conserved_count = [
                row[phyloP100_column] > 0.5 if pd.notna(row[phyloP100_column]) else None,
                row[phyloP30_column] > 1.2 if pd.notna(row[phyloP30_column]) else None,
                row[phastCons_column] > 0.5 if pd.notna(row[phastCons_column]) else None,
                row[eigen_column] > 0 if pd.notna(row[eigen_column]) else None,
                row[gerp_column] > 2 if pd.notna(row[gerp_column]) else None
            ]

            # Count occurrences of True, False, and N/A of above
            true_count = sum(value is True for value in conserved_count)
            false_count = sum(value is False for value in conserved_count)
            na_count = len(conserved_count) - true_count - false_count

            # TRUE implies the condition is satisfied, i.e. conserved
            # FALSE implies the condition is satisfied, i.e. not_conserved
            # [if pd.notna..] was included due to the avaiability of N/A (seperate na_count was taken)

            # ************* ADOPTING MAJORITY VOTING ALGORITHM *****************

            # Use simple if-else logic to determine conservation status
            if true_count > false_count:
                results.append((index, 'conserved'))
            elif false_count > true_count:
                results.append((index, 'not_conserved'))
            elif na_count > true_count and na_count > false_count:
                results.append((index, 'N/A'))
            elif true_count == false_count:
                results.append((index, 'ambiguous_conservation'))

        else:
            results.append((index, 'N/A'))

    return results
