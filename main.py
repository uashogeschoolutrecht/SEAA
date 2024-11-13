import os 
import pandas as pd
from functions.loadSEAAdata import loaddata

## Import NSE open answers
logedin_user = os.getlogin()
path = f"C:\\Users\\{logedin_user}\\Stichting Hogeschool Utrecht\\FCA-DA-P - Analytics\\Open antwoorden\\"
file_name = "demo.csv"
nseant_df = loaddata(path, file_name)

## Import dictionaries
# Safe words dictionaries (Dutch dictionary + whitelist)
from functions.loadSEAAdata import loaddict
word_list_df = loaddict(path=path, file_name="wordlist.txt", type='known')
whitelist_df = loaddict(path=path, file_name='whitelist_demo.txt')
# merge all words that are considered safe
word_list_df = pd.concat([word_list_df, whitelist_df], ignore_index=True)

## Flag words (privacy-related words: illness, disabilities, names, blacklist)
illness_df = loaddict(path=path, file_name='illness.txt', type='illness')
study_disability_df = loaddict(path=path, file_name='studiebeperking.txt', type='disability')
first_name_df = loaddict(path=path, file_name='firstnames.txt', type='name')
blacklist_df = loaddict(path=path, file_name='blacklist.txt', type = 'blacklist')
# merge all wordlists that should be flagged into one dataframe
flag_df = pd.concat([illness_df, blacklist_df, study_disability_df, first_name_df], ignore_index=True)
del illness_df, blacklist_df, study_disability_df, first_name_df

## Run SEAA
from functions.SEAA import SEAA
result_df = SEAA(nseant_df, word_list_df,flag_df)