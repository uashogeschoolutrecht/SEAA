import os
import pandas as pd
from functions.loadSEAAdata import loaddata, loaddict
from functions.SEAA import SEAA
from langdetect import detect
from functions.AVG_list import AVG_list
from functions.expand_dicts import expand_dicts


def detect_language(text):
    try:
        return detect(text)
    except:
        return None

def main(path, file_name):
    # Set location using SHPFCA class
    nseant_df = loaddata(path, file_name)

    # Import dictionaries
    word_list_df = loaddict(path=path, file_name="wordlist.txt", type='known')
    whitelist_df = loaddict(path=path, file_name='whitelist_demo.txt')
    word_list_df = pd.concat([word_list_df, whitelist_df], ignore_index=True)

    # Flag words
    illness_df = loaddict(path=path, file_name='illness.txt', type='illness')
    study_disability_df = loaddict(path=path, file_name='studiebeperking.txt', type='disability')
    first_name_df = loaddict(path=path, file_name='firstnames.txt', type='name')
    blacklist_df = loaddict(path=path, file_name='blacklist.txt', type='blacklist')
    flag_df = pd.concat([illness_df, blacklist_df, study_disability_df, first_name_df], ignore_index=True)
    del illness_df, blacklist_df, study_disability_df, first_name_df

    # Run SEAA
    result_df = SEAA(nseant_df, word_list_df, flag_df)

    # Save results to output file
    file_name = 'SEAA_output.csv'
    result_df.to_csv(f'{path}{file_name}', sep=';')

    # Language detection
    result_df['language'] = result_df['answer_clean'].apply(detect_language)

    # Create list of unknown words for review
    avg_words_df = AVG_list(result_df[result_df["language"] != 'en'])
    avg_words_df = avg_words_df.merge(flag_df, 'left', left_on='AVG_woord', right_on='words')
    avg_words_df = avg_words_df[avg_words_df['words'].isna()].drop(columns='words')

    # Save unknown words to file
    file_name = 'avg_words_count.csv'
    avg_words_df.to_csv(f'{path}{file_name}', sep=';')

    # Expand upon the blacklist and/or whitelist
    whitelist_df, blacklist_df = expand_dicts(avg_words_df, whitelist_df, blacklist_df)

    # Save lists to file
    whitelist_df.to_csv(f'{path}//dict//whitelist.txt', index=False)
    blacklist_df.to_csv(f'{path}//dict//blacklist.txt', index=False)


if __name__ == "__main__":
    # SET THE PATH AND FILE NAME
    logedin_user = os.getlogin()
    path = f"C:\\Users\\{logedin_user}\\OneDrive - Stichting Hogeschool Utrecht\\Documents\\git repos\\SEAA\\"
    file_name = "demo.csv"
    main(path, file_name)
