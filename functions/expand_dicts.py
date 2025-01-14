import pandas as pd

def get_ja_nee_blacklist_choice(question: str) -> str:
    """
    Get user input to categorize a word (yes/no/blacklist).
    
    Args:
        question: The prompt to show the user
    Returns:
        str: 'y' for yes, 'n' for no, 'b' for blacklist
    """
    while True:
        reply = input(f"{question} (j/n/blacklist): ").lower().strip()
        if reply.startswith('j'):
            return 'y'
        elif reply == 'blacklist':
            return 'b'
        elif reply.startswith('n'):
            return 'n'
        print('Onjuiste input antwoord moet j/n/blacklist zijn!')

def expand_dicts(avg_words_df: pd.DataFrame, 
                 whitelist_df: pd.DataFrame, 
                 blacklist_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Let users categorize words into whitelist or blacklist based on their input.
    
    Args:
        avg_words_df: DataFrame containing words and their frequencies
        whitelist_df: DataFrame containing whitelisted words
        blacklist_df: DataFrame containing blacklisted words
    Returns:
        tuple: Updated (whitelist_df, blacklist_df)
    """
    for idx in avg_words_df.head(15).index:
        word = avg_words_df['AVG_woord'][idx]
        count = avg_words_df['Count'][idx]
        
        prompt = f"{word} kwam {count} keer voor in de open antwoorden.\nWil je dit woord toevoegenaan de whitelist?"
        user_choice = get_ja_nee_blacklist_choice(prompt)
        word_df = pd.DataFrame({'words': [word]})
        
        if user_choice == 'y':
            whitelist_df = pd.concat([whitelist_df, word_df], axis=0)
            print(f'Woord "{word}" is toegevoegd aan de whitelist')
        elif user_choice == 'b':
            blacklist_df = pd.concat([blacklist_df, word_df], axis=0)
            print(f'Woord "{word}" is toegevoegd aan de blacklist')
        else:
            print(f'Woord "{word}" is overgeslagen')
    
    return whitelist_df, blacklist_df