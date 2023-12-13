## Load data
def loaddata(path, file_name):
    '''Load csv file containing one column of open answers (strings), clean data and add columns.'''
    import os
    import pandas as pd

    # Import NSE open answers
    df = pd.read_csv(f'{path}{file_name}', sep =';')
    
    # Clean data
    df['Antwoord_clean'] = df['Antwoord'].str.lower()
    df['Antwoord_clean'] = df['Antwoord_clean'].str.replace(r"([0-9])", "", regex=True)
    
    # Add columns: 1 for AVG sensitivity and 1 to track AVG sensitive words.
    ## AVG sensitivity is either 0 or 1. preset 1 means sensitive.
    df['AVG_gevoelig'] = 1
    ## Column to print words present in answers but not in imported dictionary.
    df['gevoelige_woorden'] = ''

    return df

## Load dictionary