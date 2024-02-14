## Load data
def loaddata(path, file_name):
    '''Load csv file containing one column of open answers (strings), cleans the data 
    and add columns.'''
    import pandas as pd

    # Import NSE open answers
    path = f"{path}data\\"
    df = pd.read_csv(f'{path}{file_name}', sep =';')
    
    # Clean data
    df['Antwoord_clean'] = df['Antwoord'].str.lower()
    df['Antwoord_clean'] = df['Antwoord_clean'].str.replace(r"([0-9])", "", regex=True)
    
    # Add columns: 1 for AVG sensitivity and 1 to track AVG sensitive words.
    ## AVG sensitivity is either 0 or 1. preset 1 means sensitive.
    df['AVG_gevoelig'] = 1
    ## Column to print words present in answers but not in imported dictionary.
    df['gevoelige_woorden'] = ''
    df['flagged words'] = ''

    return df

## Load dictionary
def loaddict(path, file_name):
    '''Load text file containing dictionary (i.e. words of the Dutch language).'''
    import pandas as pd
    path = f"{path}dict\\"
    df_dict = pd.read_csv(f"{path}{file_name}", sep =';')

    return df_dict