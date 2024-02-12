import pandas as pd

def AVG_list(df):
    '''Retrieve list of flagged AVG words and write unique values
    to CSV with count.'''
    avg_list = df['gevoelige_woorden'].tolist()
    while('' in avg_list):
        avg_list.remove('')

    avg_list_def = []
    for item in avg_list:
        words = item.split(", ")
        avg_list_def.extend(words)

    # Create datframe containing all AVG words with count
    word_count = pd.Series(avg_list_def).value_counts()
    avg_words_df = pd.DataFrame({'AVG_woord': word_count.index, 'Count': word_count.values})

    csv_file_path = 'avg_words_count.csv'
    avg_words_df.to_csv(csv_file_path, index=False) 