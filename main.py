import numpy as np
import pandas as pd
from src.load_seaa_data import load_data, load_dictionary
from src.SEAA import SEAA
from langdetect import detect
from src.AVG_list import AVG_list
from src.translator_ import translate_large_text
import re  # Add this import at the top since it's used for email pattern matching


def translate_non_dutch_responses(input_df, progress_callback=None):
    """
    Translates non-Dutch responses to Dutch.
    
    Args:
        input_df (DataFrame): DataFrame containing responses with 'language' and 'answer_clean' columns
        progress_callback (callable, optional): Function to call with progress updates
        
    Returns:
        DataFrame: Updated DataFrame with translated responses
    """
    # Language detection    
    def detect_language(text):
        try:
            return detect(text)
        except:
            return None

    input_df['language'] = input_df['answer_clean'].apply(detect_language)
    
    if progress_callback:
        progress_callback(25, "preparation")

    # Count how many translations are needed
    non_dutch_count = len(input_df[(pd.notna(input_df['language'])) & 
                                  (input_df['language'] != 'nl') & 
                                  (input_df['language'] != 'af') & 
                                  (pd.notna(input_df['answer_clean']))])
    
    # Create a copy of the DataFrame to avoid modifying during iteration
    df_copy = input_df.copy()
    
    
    if non_dutch_count > 0:
        if progress_callback:
            progress_callback(0, "translation")
            
        # Create a counter for translations
        translation_counter = 0

        for index, row in df_copy.iterrows(): 
            if pd.notna(row['language']) and row['language'] != 'nl' and row['language'] != 'af' and pd.notna(row['answer_clean']):
                # Translate the text
                translated = translate_large_text(
                    row['answer_clean'], 
                    source_lang=row['language'], 
                    target_lang='nl'
                )
                
                # Update the original DataFrame with the translated text
                df_copy.at[index, 'answer_clean'] = translated
                
                # Update progress
                translation_counter += 1
                if progress_callback:
                    progress = (translation_counter / non_dutch_count) * 100
                    progress_callback(progress, "translation")
    
    return df_copy


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

    df = load_data(path, input_file)
    input_df = df.head(limit)

    # Report progress if callback is provided
    if progress_callback:
        progress_callback(0, "preparation")

    # Translate non-Dutch responses
    input_df = translate_non_dutch_responses(input_df, progress_callback)
    
    if progress_callback:
        progress_callback(50, "preparation")

    # Detect and censor email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    for index, row in input_df.iterrows():
        if pd.notna(row['answer_clean']):
            emails_found = re.findall(email_pattern, row['answer_clean'])
            if emails_found:
                censored_text = row['answer_clean']
                for email in emails_found:
                    censored_text = re.sub(re.escape(email), '[EMAIL]', censored_text)
                input_df.loc[index, 'answer_clean'] = censored_text
                print(f"Email found in row {index}: {emails_found}")

    # Remove numbers longer than 2 digits
    input_df['answer_clean'] = input_df['answer_clean'].str.replace(r'\b\d{3,}\b', '', regex=True)
    
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
    
    if progress_callback:
        progress_callback(75, "preparation")

    if progress_callback:
        progress_callback(100, "preparation")

    result_df = SEAA(input_df, word_list_df, flag_df, limit=limit, progress_callback=progress_callback)

    # Get all avg words that are not flagged yet
    avg_words_df = AVG_list(result_df[result_df["language"] == 'nl'].copy(), flag_df)
    avg_words_df = avg_words_df.merge(flag_df, 'left', left_on='AVG_woord', right_on='words')
    avg_words_df = avg_words_df[avg_words_df['words'].isna()].drop(columns='words')



    return result_df, avg_words_df

