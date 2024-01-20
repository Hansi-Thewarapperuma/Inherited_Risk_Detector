'''
Evaluation rules accomplished through a scoring system
genetic variant scoring system
Input: TSV file
Output: filtered entries with the highest and second highest total scores (i.e.: pathogenic and likely pathogenic disease causing variants)

Author: Hansi Thewarapperuma
Date: 25/12/2023
'''

import MAF
import Clin_sig
import Cons_score
import Func_pred
import Gen_context
import file_process
import Quality

# main method
if __name__ == '__main__':
    # obtain the user input fasta file
    user_tsv = input('Enter your generated TSV file: ')

    input_variants_df = file_process.tsv_to_df(user_tsv)

    # in silico functional predictions - output: list of tuples containing the index and evaluation
    functional_pred = Func_pred.in_silico_functional_predictions(input_variants_df)
    if functional_pred is None:
        functional_pred = []

    # conservation score - output: list of tuples containing the index and evaluation
    consv_score = Cons_score.conservation_scores(input_variants_df)
    if consv_score is None:
        consv_score = []

    # clinical significance - output: list of tuples containing the index and evaluation
    clinical_sig_scores = Clin_sig.evaluate_clinical_significance(input_variants_df)
    if clinical_sig_scores is None:
        clinical_sig_scores = []

    # minor allele frequency - output: list of tuples containing the index and evaluation
    af_output = MAF.evaluate_minor_allele_freq(input_variants_df)
    if af_output is None:
        af_output = []

    # genomic context - output: list of tuples containing the index and evaluation
    impact_output = Gen_context.evaluate_genomic_context(input_variants_df)
    if impact_output is None:
        impact_output = []

     # Quality - Output: output: list of tuples containing the index and quality type
    quality_status = Quality.evaluate_quality(input_variants_df)
    if quality_status is None:
        quality_status = []

    # Assuming you have obtained lists of tuples from each function
    # functional_pred, consv_score, clinical_sig_scores, af_output, impact_output

    # Initialize a dictionary to store results
    results_dict = {}

    # Merge results using the common index
    for result_list in [functional_pred, consv_score, clinical_sig_scores, af_output, impact_output, quality_status]:
        for result_tuple in result_list:
            index = result_tuple[0]
            evaluation = result_tuple[1:]

            # Add or update the dictionary with the evaluation
            if index in results_dict:
                results_dict[index].extend(evaluation)
            else:
                results_dict[index] = list(evaluation)

    # *********************** EVALUATION-RULES *************************************

    # highest score 1 given to the highest priority evaluation value which ensures pathogenicity and vice versa
    # All the evaluaton values were given the same priority


    # 1 was assigned to the above terms as they determine the pathogenicity of the variant
    # -1 assigned to the opposite terms as they contradict the pathogenicity of the variant
    # 0 was assigned to the neutral terms which have no evidence about pathogenicity


    # Define a scoring system       *********** VUS SCORE **********************
    score_dict = {
        'considerable_impact': 1,
        'deleterious': 1,
        'rare': 1,
        'conserved': 1,
        'pathogenic': 1,
        'quality' : 1,
        'vus': 0,

        'no_considerable_impact': -1,
        'not_deleterious': -1,
        'common': -1,
        'not_conserved': -1,
        'benign': -1,
        'less_quality' : -1,

        'unresolved_clinical_significance': 0,
        'N/A': 0,
        'ambiguous_conservation': 0,
        'ambiguous_deleteriousness': 0
    }


    # Calculate the total score for each entry
    def calculate_score(evaluations):
        total_score = sum(score_dict[eval_value] for eval_value in evaluations)
        return total_score


    # Filter out entries with 'N/A' as all the evaluation values
    # filtered_results_dict = {index: evaluations for index, evaluations in results_dict.items() if
    #                          'N/A' not in evaluations}

    # Sort entries based on total score
    sorted_results = sorted(results_dict.items(), key=lambda x: calculate_score(x[1]), reverse=True)

    # Print or use the sorted results as needed (********** COMMENT OUT TO PRINT ALL **************)
    # for index, evaluations in sorted_results:
    #     print(f"Index: {index}, Evaluations: {evaluations}, Total Score: {calculate_score(evaluations)}")

    # Find the highest total score
    if sorted_results:
        highest_total_score = calculate_score(sorted_results[0][1])
    else:
        highest_total_score = 0

    # Filter out entries with the highest total score
    filtered_highest_score_results = {index: evaluations for index, evaluations in sorted_results if
                                      calculate_score(evaluations) == highest_total_score}

    # Print or use the filtered results as needed : HIGHEST SCORE
    for index, evaluations in filtered_highest_score_results.items():
        print(f"Index: {index}, Evaluations: {evaluations}, Total Score: {calculate_score(evaluations)}")

    #  ****** IN CASE IF YOU WANT TO CONSIDER THE SECOND HIGHEST SCORE*******
    # Find the second-highest total score
    if len(sorted_results) > 1:
        try:
            second_highest_total_score = calculate_score(next(
                evaluations for index, evaluations in sorted_results[1:] if
                calculate_score(evaluations) != highest_total_score))
        except StopIteration:
            second_highest_total_score = 0
    else:
        second_highest_total_score = 0

    # Filter out entries with the second-highest total score
    filtered_second_highest_score_results = {index: evaluations for index, evaluations in sorted_results if
                                             calculate_score(evaluations) == second_highest_total_score}

    # Print or use the filtered results as needed: SECOND HIGHEST SCORE
    for index, evaluations in filtered_second_highest_score_results.items():
        print(f"Index: {index}, Evaluations: {evaluations}, Total Score: {calculate_score(evaluations)}")