
# A function to get the names of the medewerkers from the database
# and convert them to a list of names

from functions.db_functions import DB
import pandas as pd
from functions.load_seaa_data import load_dictionary

def get_medewerkers_names():
    # Get the names of the medewerkers from the database
    db = DB()
    
    # Read SQL query from file
    with open('functions\\sql\\medewerkes.sql', 'r') as file:
        sql_query = file.read()
        
    names = db.read_from_db(otap='prod',sql_query=sql_query)
    
    # Remove SAMENGESTELDE NAAM from NAAM to get VOORNAAM, ignoring NaN values
    names['VOORNAAM'] = names.apply(lambda row: row['NAAM'].replace(str(row['SAMENGESTELDE NAAM']), '')\
        if pd.notna(row['SAMENGESTELDE NAAM']) else row['NAAM'], axis=1).str.strip()
    names['VOORNAAM'] = names.apply(lambda row: row['VOORNAAM'].replace(str(row['VOORVOEGSELS SAMENGESTELD']), '')\
        if pd.notna(row['VOORVOEGSELS SAMENGESTELD']) else row['VOORNAAM'], axis=1).str.strip()
    names['VOORNAAM'] = names.apply(lambda row: row['VOORNAAM'].replace(str(row['VOORVOEGSELS SAMENGESTELD']), '')\
        if pd.notna(row['VOORVOEGSELS SAMENGESTELD']) else row['VOORNAAM'], axis=1).str.strip()
    names['VOORNAAM'] = names['VOORNAAM'].str.replace(', ', '')
    names_list = names['VOORNAAM'].tolist() + names['SAMENGESTELDE NAAM'].tolist()
    names_list = list(set(names_list))
    names_list = [names for names in names_list if str(names) != 'nan']
    names_list = [names for names in names_list if names is not None]
    names_list_keep = [name for name in names_list if len(name) > 5]
    
    names_list_df = pd.DataFrame(names_list_keep)
    names_list_df.columns = ['words']
    names_list_df['words'] = names_list_df['words'].str.lower()
    
    # Check if words are in the wordlist
    word_list_df = load_dictionary(file_name="wordlist.txt", dict_type='known')
    word_list_df['words'] = word_list_df['words'].str.lower()
    
    # Remove words that are in the wordlist
    names_list_df = names_list_df[~names_list_df['words'].isin(word_list_df['words'])]
    
    # Write names to file
    names_list_df.to_csv(f'dict//medewerkers_names.txt', index=False)