import pandas as pd

def AVG_list(df):
    '''Retrieve list of flagged AVG words and write unique values
    to CSV with count.'''
    avg_list = df['unknown words'].tolist()
    
    # Clean wordlist from empty values
    while('' in avg_list):
        avg_list.remove('')

    # For all items in the word list, split the words
    avg_list_def = []
    for item in avg_list:
        words = item.split(", ")
        avg_list_def.extend(words)

    # Create dataframe containing all AVG words with count
    word_count = pd.Series(avg_list_def).value_counts()
    avg_words_df = pd.DataFrame({'AVG_woord': word_count.index, 'Count': word_count.values})

    return avg_words_df