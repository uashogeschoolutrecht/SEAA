"""
Data loading and preprocessing functions for SEAA.
"""

import os
import re
import pandas as pd
from typing import Literal
from langdetect import detect


def _detect_language(text: str) -> str | None:
    """Detect the language of a text string."""
    try:
        return detect(text)
    except:
        return None


def _prepare_text(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare text data by detecting language and creating lowercase clean version.
    
    Args:
        df: DataFrame with 'Answer' column
        
    Returns:
        DataFrame with added 'answer_clean' and 'language' columns
    """
    df_copy = df.copy()
    df_copy['answer_clean'] = df_copy['Answer'].str.lower()
    df_copy['language'] = df_copy['answer_clean'].apply(_detect_language)
    return df_copy


def load_data(path: str, file_name: str) -> pd.DataFrame:
    """
    Load and clean CSV file containing open-ended answers.
    
    Args:
        path: Directory path containing the CSV file
        file_name: Name of the CSV file
    
    Returns:
        DataFrame with cleaned answers and additional columns
    """
    # Load CSV file
    df = pd.read_csv(os.path.join(path, file_name), sep=';', encoding='utf-8-sig')
    
    # Detect language and prepare clean text
    df = _prepare_text(df)
    
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

    # Clean text: remove numbers, punctuation, normalize whitespace
    df['answer_clean'] = (df['answer_clean']
        .str.replace(r'\b\d{3,}\b', '', regex=True)  # Remove numbers longer than 2 digits
        .str.lower()
        .str.replace(r'[0-9]', '', regex=True)       # Remove all digits
        .str.replace(r'[^\w\s]', ' ', regex=True)    # Remove punctuation
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)        # Normalize whitespace
    )
    
    # Initialize tracking columns
    df['contains_privacy'] = 1
    df['unknown_words'] = ''
    df['flagged_words'] = ''

    return df


def load_dictionary(file_name: str, dict_type: Literal['known', 'illness'] | str = '') -> pd.DataFrame:
    """
    Load dictionary file containing word lists.
    
    Args:
        file_name: Name of the dictionary file
        dict_type: Type of dictionary ('known' for safe words, or flag type like 'illness', 'name', etc.)
    
    Returns:
        DataFrame containing dictionary words
    """
    dictionary_df = pd.read_csv(os.path.join('dict', file_name), sep=';', encoding='utf-8-sig')
    
    if dict_type != 'known':
        dictionary_df['words'] = dictionary_df['words'].str.lower()
        dictionary_df['dict_type'] = dict_type        

    # Keep 'ALS' (disease) uppercase to distinguish from 'als' (Dutch word for 'if/as')
    if dict_type == "illness":
        dictionary_df = dictionary_df.replace('als', 'ALS')
    
    return dictionary_df