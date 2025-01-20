import pandas as pd
from functions.load_seaa_data import load_data, load_dictionary
from functions.nse.transform_raw_data import transform_nse_data
from functions.SEAA import SEAA
from langdetect import detect
from functions.AVG_list import AVG_list
from functions.expand_dicts import expand_dicts
from functions.get_medewerkers_names import get_medewerkers_names

def main(path, file_name=None, limit=-1,input_file_name=None):
    """
    Process and analyze student evaluation answers (SEAA) data.
    
    Args:
        path (str): Directory path where input/output files are stored
        file_name (str): Name of the file to process (if NSE data is already transformed)
        input_file_name (str, optional): Name of raw NSE data file to transform. If provided,
            transforms the data before processing
    
    The function:
    - Transforms NSE data if raw input is provided
    - Loads and processes dictionaries (word lists, whitelists, and flag words)
    - Performs SEAA analysis on the text
    - Detects language of responses
    - Generates and saves lists of unknown words
    - Updates and saves whitelist/blacklist dictionaries
    """
    
    # If NSE transform raw data
    if input_file_name is not None:
        transform_nse_data(
            input_path=path,
            input_file_name=input_file_name,
        )
        file_name='nse_transformed.csv'
    
    nseant_df = load_data(path, file_name)
    
    # Import latast medewerkers names
    # get_medewerkers_names()

    # Import dictionaries
    word_list_df = load_dictionary(file_name="wordlist.txt", dict_type='known')
    whitelist_df = load_dictionary(file_name='whitelist.txt', dict_type='known')
    
    word_list_df = pd.concat([word_list_df, whitelist_df], ignore_index=True)

    # Flag words
    flag_df = pd.DataFrame()
    for file_name,file_type in [('illness.txt', 'illness'), ('studiebeperking.txt', 'disability'), ('firstnames.txt', 'name'), ('medewerkers_names.txt', 'medewerkers_names'), ('blacklist.txt', 'blacklist')]:
        temp_df = load_dictionary(file_name=file_name, dict_type=file_type)
        flag_df = pd.concat([flag_df, temp_df], ignore_index=True)
    del temp_df

    result_df = SEAA(nseant_df, word_list_df, flag_df,limit=1000)

    # Save results to output file
    file_name = '\\SEAA_output.csv'
    result_df.to_csv(f'{path}{file_name}', sep=';')

    # Language detection    
    def detect_language(text):
        try:
            return detect(text)
        except:
            return None

    result_df['language'] = result_df['answer_clean'].apply(detect_language)
    
    # get all avg words that are not flagged yet
    avg_words_df = AVG_list(result_df[result_df["language"] == 'nl'].copy(),flag_df)
    avg_words_df = avg_words_df.merge(flag_df, 'left', left_on='AVG_woord', right_on='words')
    avg_words_df = avg_words_df[avg_words_df['words'].isna()].drop(columns='words')

    # Save unknown words to file
    file_name = 'avg_words_count.csv'
    avg_words_df.to_csv(f'{path}{file_name}', sep=';')

    # Import blacklist
    blacklist_df = load_dictionary(file_name='blacklist.txt', dict_type='known')

    # Expand upon the blacklist and/or whitelist
    whitelist_df, blacklist_df = expand_dicts(avg_words_df, whitelist_df, blacklist_df)
    
    # Save lists to file
    whitelist_df.to_csv(f'dict//whitelist.txt', index=False) 
    blacklist_df.to_csv(f'dict//blacklist.txt', index=False)



file_name = "nse2023.csv"
path = r'C:\Users\fraukje.coopmans\Stichting Hogeschool Utrecht\FCA-DA-P - Analytics\Open antwoorden\data'
main(path, file_name, input_file_name=file_name)