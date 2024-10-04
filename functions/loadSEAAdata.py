## Load data
def loaddata(path, file_name):
    '''Load csv file containing one column of open answers (strings), cleans the data 
    and add columns.'''
    import pandas as pd

    # Import NSE open answers
    path = f"{path}data\\"
    df = pd.read_csv(f'{path}{file_name}', sep =';')
    
    # Clean data
    df['answer_clean'] = df['Answer'].str.lower()
    df['answer_clean'] = df['answer_clean'].str.replace(r"([0-9])", "", regex=True)
    
    # Add columns: 1 for AVG sensitivity and 1 to track AVG sensitive words.
    ## AVG sensitivity is either 0 or 1. preset 1 means sensitive.
    df['contains_privacy'] = 1
    ## Column to print words present in answers but not in imported dictionary.
    df['unknown_words'] = ''
    df['flagged_words'] = ''

    return df

## Load dictionary
def loaddict(path, file_name, type = ''):
    '''Load text file containing dictionary (i.e. words of the Dutch language).'''
    import pandas as pd
    path = f"{path}dict\\"
    df_dict = pd.read_csv(f"{path}{file_name}", sep =';')

    # For the illness dictionary convert words to smallcase
    if type == "illness":
        df_dict['words'] = df_dict['words'].str.lower()
        # Exception for illness ALS, which in small cases is a common Dutch word
        df_dict = df_dict.replace('als', 'ALS')

    return df_dict