import pandas as pd
import os
from typing import Union, Literal
from src.translator_ import translate_large_text
from langdetect import detect
import time
import re

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
    df_copy = input_df.copy()
    
    df_copy['answer_clean'] = df_copy['Answer'].str.lower()

    df_copy['language'] = df_copy['answer_clean'].apply(detect_language)
    
    if progress_callback:
        progress_callback(25, "preparation")
        time.sleep(1)
    
    if progress_callback:
        progress_callback(50, "preparation")
        time.sleep(1)

    # Count how many translations are needed
    # non_dutch_count = len(df_copy[(pd.notna(df_copy['language'])) & 
    #                               (df_copy['language'] != 'nl') & 
    #                               (df_copy['language'] != 'af') & 
    #                               (pd.notna(df_copy['answer_clean']))])
    
    # # Create a copy of the DataFrame to avoid modifying during iteration
   

    # if non_dutch_count > 0:
    #     if progress_callback:
    #         progress_callback(0, "translation")
            
    #     # Create a counter for translations
    #     translation_counter = 0

    #     for index, row in df_copy.iterrows(): 
    #         if pd.notna(row['language']) and row['language'] != 'nl' and row['language'] != 'af' and pd.notna(row['answer_clean']):
    #             # Translate the text
    #             translated = translate_large_text(
    #                 row['answer_clean'], 
    #                 source_lang=row['language'], 
    #                 target_lang='nl'
    #             )
                
    #             # Update the original DataFrame with the translated text
    #             df_copy.at[index, 'answer_clean'] = translated
                
    #             # Update progress
    #             translation_counter += 1
    #             if progress_callback:
    #                 progress = (translation_counter / non_dutch_count) * 100
    #                 progress_callback(progress, "translation")
    
    # if progress_callback:
    #     progress_callback(100, "translation")
    #     time.sleep(1)

    # if progress_callback:
    #     progress_callback(75, "preparation")
    #     time.sleep(1)

    # if progress_callback:
    #     progress_callback(100, "preparation")
    #     time.sleep(1)

    return df_copy

def load_data(path: str, file_name: str, progress_callback=None) -> pd.DataFrame:
    """
    Load and clean CSV file containing open-ended answers.
    
    Args:
        path: Directory path containing the CSV file
        file_name: Name of the CSV file
    
    Returns:
        DataFrame with cleaned answers and additional columns
    """
    # Import NSE open answers
    df = pd.read_csv(os.path.join(path, file_name), sep =';', encoding='utf-8-sig')
    df = translate_non_dutch_responses(df, progress_callback)
    
        # Detect and censor email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    for index, row in df.iterrows():
        if pd.notna(row['answer_clean']):
            emails_found = re.findall(email_pattern, row['answer_clean'])
            if emails_found:
                censored_text = row['answer_clean']
                for email in emails_found:
                    censored_text = re.sub(re.escape(email), 'emailadressreplacer', censored_text)
                df.loc[index, 'answer_clean'] = censored_text
                print(f"Email found in row {index}: {emails_found}")

    # Remove numbers longer than 2 digits
    df['answer_clean'] = df['answer_clean'].str.replace(r'\b\d{3,}\b', '', regex=True)

    # Clean data
    df['answer_clean'] = df['answer_clean'].str.lower()
    
    # Remove numbers
    df['answer_clean'] = df['answer_clean'].str.replace(r"([0-9])", "", regex=True)
    
    # Remove all symbols/punctuation marks
    df['answer_clean'] = df['answer_clean'].str.replace(r'[^\w\s]', ' ', regex=True)
    
    # Trim whitespace
    df['answer_clean'] = df['answer_clean'].str.strip()
    # Remove multiple spaces
    df['answer_clean'] = df['answer_clean'].str.replace(r'\s+', ' ', regex=True)
    
    # Initialize tracking columns
    df['contains_privacy'] = 1
    df['unknown_words'] = ''
    df['flagged_words'] = ''

    return df

def load_dictionary(file_name: str, dict_type: Union[Literal['known'], Literal['illness'], str] = '') -> pd.DataFrame:
    """
    Load dictionary file containing word lists.
    
    Args:
        file_name: Name of the dictionary file
        dict_type: Type of dictionary ('known' or 'illness' for special processing)
    
    Returns:
        DataFrame containing dictionary words
    """
    dictionary_df = pd.read_csv(os.path.join('dict', file_name), sep =';', encoding='utf-8-sig')
    
    if dict_type != 'known':
        dictionary_df['words'] = dictionary_df['words'].str.lower()
        dictionary_df['dict_type'] = dict_type        

    if dict_type == "illness":
        dictionary_df = dictionary_df.replace('als', 'ALS')
        
    
    return dictionary_df