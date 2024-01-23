'''
Function: Evaluation through In-silico functional prediction criterion
Input: Dataframe
Output: A list of tuples containing index and evaluation (deleterios, not_deleterious, N/A)

Author: Hansi Thewarapperuma
Date: 10/12/2023
'''
import pandas as pd

def in_silico_functional_predictions(input_variants_df):

    # Define columns
    polyphen_column = 'dbNSFP_Polyphen2_HDIV_pred'
    sift_column = 'dbNSFP_SIFT_pred'
    mutationtaster_column = 'dbNSFP_MutationTaster_pred'
    provean_column = 'dbNSFP_PROVEAN_pred'
    cadd_column = 'dbNSFP_CADD_phred_hg19'
    fathmm_column = 'dbNSFP_FATHMM_pred'

    # create a list including the above-mentioned columns
    func_pred_columns = [polyphen_column, sift_column, mutationtaster_column, provean_column, cadd_column,
                         fathmm_column]

    # initiate an empty list to store results
    results = []

    # Iterate through each row of the dataframe
    for index, row in input_variants_df.iterrows():

        # Check for N/A values
        na_count = row[func_pred_columns].isna().sum()

        # when all the column values are not 'N/A' ; check the conditions to determine the deleteriousness
        if na_count < len(func_pred_columns):  # If there is at least one non-N/A value
            func_pred_count = [
                'D' in str(row[polyphen_column]) or 'P' in str(row[polyphen_column]) if pd.notna(
                    row[polyphen_column]) else None,
                'D' in str(row[sift_column]) if pd.notna(row[sift_column]) else None,
                'A' in str(row[mutationtaster_column]) or 'D' in str(row[mutationtaster_column]) if pd.notna(
                    row[mutationtaster_column]) else None,
                'D' in str(row[provean_column]) if pd.notna(row[provean_column]) else None,
                'D' in str(row[fathmm_column]) if pd.notna(row[fathmm_column]) else None
            ]

            # Count occurrences of True, False, and N/A
            true_count = sum(value is True for value in func_pred_count)
            false_count = sum(value is False for value in func_pred_count)
            na_count = len(func_pred_count) - true_count - false_count

            # TRUE implies the condition is satisfied, i.e. deleterious
            # FALSE implies the condition is satisfied, i.e. not_deleterious
            # [if pd.notna..] was included due to the avaiability of N/A (seperate na_count was taken)


            # ************* ADOPTING MAJORITY VOTING ALGORITHM *****************

            # Use simple if-else logic to determine conservation status
            if true_count > false_count:
                results.append((index, 'deleterious'))
            elif false_count > true_count:
                results.append((index, 'not_deleterious'))
            elif na_count > true_count and na_count > false_count:
                results.append((index, 'N/A'))
            elif true_count == false_count:
                results.append((index, 'ambiguous_deleteriousness'))
        else:
            results.append((index, 'N/A'))

    return results