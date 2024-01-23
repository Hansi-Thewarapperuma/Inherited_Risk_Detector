import pandas as pd

def evaluate_quality(input_variants_df):

    # define relevant columns
    filter_column = 'FILTER'
    gq_column = 'GEN[*].GQ'
    qual_column = "QUAL"
    ad_column = "GEN[*].AD"
    dp_column = "GEN[*].DP"

    # Convert specified columns to numeric, handling non-numeric values
    numeric_columns = [gq_column, qual_column, ad_column, dp_column]
    input_variants_df[numeric_columns] = input_variants_df[numeric_columns].apply(pd.to_numeric, errors='coerce')

    # initiate an empty list to store results
    results = []

    # Iterate through each row of the dataframe
    for index, row in input_variants_df.iterrows():

        # Check if all the mentioned columns have 'N/A' values
        all_na = all(pd.isna(row[col]) or str(row[col]) == 'N/A' for col in numeric_columns)

        # At least one non-'N/A' value in the mentioned columns
        if not all_na:

            # low quality rows are not considered
            if 'LowQual' not in row[filter_column]:

                # Cutoff quality is set to 20 (Phred-scaled)
                if row[gq_column] >= 20:
                    results.append((index, "quality"))
                # No need for 'else' here, let it fall through to the next block
            else:
                results.append((index, 'less_quality'))
        else:
            results.append((index, 'N/A'))

    return results



