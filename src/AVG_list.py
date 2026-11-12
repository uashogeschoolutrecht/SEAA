import pandas as pd

def AVG_list(dataframe,flagged_df):
        '''Retrieve list of flagged AVG words and write unique values
        to CSV with count.'''
        
        flag_df = flagged_df.copy()
        df = dataframe.copy()
        
        avg_list = []
        for words in df['unknown_words_not_flagged']:
            avg_list.extend(words.split(', '))           
            
        # Clean wordlist from empty values
        while('' in avg_list):
            avg_list.remove('')          
        
        # Remove flagged words from avg_list
        for word in flag_df['words'].tolist():
            if word in avg_list:                    
                avg_list.remove(word)

        # For all items in the word list, split the words
        avg_list_def = []
        for item in avg_list:
            words = item.split(", ")
            avg_list_def.extend(words)

        # Create dataframe containing all AVG words with count
        word_count = pd.Series(avg_list_def).value_counts()
        avg_words_df = pd.DataFrame({'AVG_woord': word_count.index, 'Count': word_count.values})

        return avg_words_df