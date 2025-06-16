import numpy as np
import pandas as pd
from src.load_seaa_data import load_data, load_dictionary
from src.SEAA import SEAA
from src.AVG_list import AVG_list
import re  # Add this import at the top since it's used for email pattern matching
import os

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

year = 2025
input_path = r"C:\Users\AnneL\Stichting Hogeschool Utrecht\FCA-DA-P - Analytics\Open antwoorden\data\NSE"
input_file = f"nse_transformed_{year}.csv"

df = load_data(input_path, input_file)

# Import dictionaries
word_list_df = load_dictionary(file_name="wordlist.txt", dict_type='known')
whitelist_df = load_dictionary(file_name='whitelist.txt', dict_type='known')

dictionary_df = pd.concat([word_list_df, whitelist_df], ignore_index=True)

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


####SEAA

result_df = SEAA(df, dictionary_df, flag_df)

# Get all avg words that are not flagged yet
avg_words_df = AVG_list(result_df[result_df["language"] == 'nl'].copy(), flag_df)
avg_words_df = avg_words_df.merge(flag_df, 'left', left_on='AVG_woord', right_on='words')
avg_words_df = avg_words_df[avg_words_df['words'].isna()].drop(columns='words')

output_path = r"C:\Users\AnneL\Stichting Hogeschool Utrecht\FCA-DA-P - Analytics\Open antwoorden\output\NSE"
result_df.to_csv(os.path.join(output_path, f"SEAA_output_NSE_{year}_16062025.csv"), sep=';', encoding='utf-8-sig')
avg_words_df.to_csv(os.path.join(output_path, f"avg_words_count_{year}_16062025.csv"), sep=';', encoding='utf-8-sig')