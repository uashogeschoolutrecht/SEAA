import pandas as pd

def expand_dicts(avg_words_df: pd.DataFrame, 
                 whitelist_df: pd.DataFrame, 
                 blacklist_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Process words for categorization into whitelist or blacklist.
    Now returns the DataFrames without user interaction - the interaction happens via the web interface.
    
    Args:
        avg_words_df: DataFrame containing words and their frequencies
        whitelist_df: DataFrame containing whitelisted words
        blacklist_df: DataFrame containing blacklisted words
    Returns:
        tuple: Current (whitelist_df, blacklist_df)
    """
    # Save the avg_words_df for the web interface to use
    avg_words_df.to_csv('data/avg_words.csv', index=False)
    
    return whitelist_df, blacklist_df

def process_word_decision(word: str, decision: str, 
                         whitelist_df: pd.DataFrame, 
                         blacklist_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Process a single word decision from the web interface.
    
    Args:
        word: The word to categorize
        decision: 'whitelist', 'blacklist', or 'skip'
        whitelist_df: Current whitelist DataFrame
        blacklist_df: Current blacklist DataFrame
    Returns:
        tuple: Updated (whitelist_df, blacklist_df)
    """
    word_df = pd.DataFrame({'words': [word]})
    
    if decision == 'whitelist':
        whitelist_df = pd.concat([whitelist_df, word_df], ignore_index=True)
    elif decision == 'blacklist':
        blacklist_df = pd.concat([blacklist_df, word_df], ignore_index=True)
    
    return whitelist_df, blacklist_df