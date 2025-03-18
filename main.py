import numpy as np
import pandas as pd
from src.load_seaa_data import load_data, load_dictionary
from src.SEAA import SEAA
from src.AVG_list import AVG_list
import re  # Add this import at the top since it's used for email pattern matching



def main(
    path, 
    input_file=None,
    limit=-1,
    progress_callback=None
):
    """
    Process and analyze open-ended survey responses.
    
    Args:
        path (str): Directory path where input/output files are stored
        input_file (str): Name of the input CSV file to process. Must contain these columns:
            - 'answer': The text responses to analyze
            - 'respondent_id': Unique identifier for each respondent
            - 'question_id': Identifier for the question being answered
        limit (int, optional): Limit the number of responses to process. Default -1 (process all)
        progress_callback (callable, optional): Function to call with progress updates
    
    Required Input Format:
    The input CSV file must be semicolon-separated (;) and contain the following columns:
    - answer: The actual text responses
    - respondent_id: Unique identifier for each respondent
    - question_id: Identifier for the question being answered
    
    Output:
    - SEAA_output.csv: Main analysis results
    - avg_words_count.csv: List of unknown words for review
    - Updated whitelist.txt and blacklist.txt in the dict/ folder
    """
    
    if input_file is None:
        raise ValueError("Please provide an input_file name")

      # Report progress if callback is provided
    if progress_callback:
        progress_callback(0, "preparation")

    df = load_data(path, input_file,progress_callback)
    input_df = df.head(limit)
    
    # Import dictionaries
    word_list_df = load_dictionary(file_name="wordlist.txt", dict_type='known')
    whitelist_df = load_dictionary(file_name='whitelist.txt', dict_type='known')
    
    word_list_df = pd.concat([word_list_df, whitelist_df], ignore_index=True)

    # Flag words
    flag_df = pd.DataFrame()
    for file_name, file_type in [
        ('illness.txt', 'illness'), 
        ('studiebeperking.txt', 'disability'), 
        ('names.txt', 'name'), 
        ('blacklist.txt', 'blacklist'), 
        ('plaatsnamen.txt', 'plaatsnaam'),
        ('familie.txt', 'familie'),
        ('persoonlijke_omstandigheden.txt', 'persoonlijke_omstandigheden')]:
        temp_df = load_dictionary(file_name=file_name, dict_type=file_type)
        flag_df = pd.concat([flag_df, temp_df], ignore_index=True)
    del temp_df
    


    result_df = SEAA(input_df, word_list_df, flag_df, limit=limit, progress_callback=progress_callback)

    # Get all avg words that are not flagged yet
    avg_words_df = AVG_list(result_df[result_df["language"] == 'nl'].copy(), flag_df)
    avg_words_df = avg_words_df.merge(flag_df, 'left', left_on='AVG_woord', right_on='words')
    avg_words_df = avg_words_df[avg_words_df['words'].isna()].drop(columns='words')



    return result_df, avg_words_df

