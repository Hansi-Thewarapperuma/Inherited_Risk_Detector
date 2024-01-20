'''
Functon: TSV file conversion to dataframe
Input: TSV file
Output: Dataframe

Author: Hansi Thewarapperuma
Date: 25/12/2022
'''

import pandas as pd

def tsv_to_df(user_tsv):
    # input_variants_df = pd.read_csv(user_tsv, sep='\t', encoding='latin1')
    try:
        input_variants_df = pd.read_csv(user_tsv, sep='\t', encoding='latin1')
        return input_variants_df
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None

