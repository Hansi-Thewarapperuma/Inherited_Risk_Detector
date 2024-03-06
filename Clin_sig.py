'''
Function: Evaluation through clinical significance criterion (Variant interpretation in clincal context)
Input: Dataframe
Output: A list of tuples containing index and evaluation (clinically_significant, not_clinically_significant, unresolved_clinica_significance, N/A)

Author: Hansi Thewarapperuma
date: 18/12/2023
'''


def evaluate_clinical_significance(input_variants_df):

    # define the columns of TSV
    clnsig_column = 'CLNSIG'

    # allocate customised scores for expected variant interpretations based on priority
    pathogenic_score = 1
    vus_score = 0.1
    benign_score = 0.01

    # initiate an empty list to store results
    results = []

    # iterate through each row of the dataframe
    for index, row in input_variants_df.iterrows():

        # initially each column values were assigned to 0
        clnsig_score = 0

        # FOR clnsig_column
        # exclude missing values
        if str(row[clnsig_column]).lower() != 'n/a':
            # if 'conflicting_interpretations_of_pathogenicity' in str(row[clnsig_column]).lower():
            #     clnsig_score = 0.05
            # when the condition is true; the clnsig_score is assigned with corresponding variant interpretation score
            if 'pathogenic' in str(row[clnsig_column]).lower():
                clnsig_score = pathogenic_score
            elif 'benign' in str(row[clnsig_column]).lower():
                clnsig_score = benign_score
            elif 'uncertain_significance' in str(row[clnsig_column]).lower():
                clnsig_score = vus_score


        # value comparison ; both values should be similar to interpret the pathogenicity, otherwise its conflicting

        if clnsig_score == 1:
            results.append((index, 'pathogenic'))
        elif clnsig_score == 0.1:
            results.append((index, 'vus'))
        elif clnsig_score == 0.01:
            results.append((index, 'benign'))
        elif clnsig_score == 0:
            results.append((index, 'N/A'))


    return results
