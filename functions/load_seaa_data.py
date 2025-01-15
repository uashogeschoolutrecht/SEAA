import pandas as pd
import os
from typing import Union, Literal

def load_data(path: str, file_name: str) -> pd.DataFrame:
    """
    Load and clean CSV file containing open-ended answers.
    
    Args:
        path: Directory path containing the CSV file
        file_name: Name of the CSV file
    
    Returns:
        DataFrame with cleaned answers and additional columns
    """
    # Import NSE open answers
    df = pd.read_csv(os.path.join(path, file_name), sep =';', encoding='utf-8')
    
    # Clean data
    df['answer_clean'] = df['Answer'].str.lower()
    df['answer_clean'] = df['answer_clean'].str.replace(r"([0-9])", "", regex=True)
    
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
    dictionary_df = pd.read_csv(os.path.join('dict', file_name), sep =';', encoding='utf-8')
    
    if dict_type != 'known':
        dictionary_df['words'] = dictionary_df['words'].str.lower()
        dictionary_df['dict_type'] = dict_type        

    if dict_type == "illness":
        dictionary_df = dictionary_df.replace('als', 'ALS')
        
    
    return dictionary_df