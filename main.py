import os 
import pandas as pd
from functions.loadSEAAdata import loaddata

## Import NSE open answers
logedin_user = os.getlogin()
path = f"C:\\Users\\{logedin_user}\\Stichting Hogeschool Utrecht\\FCA-DA-P - Analytics\\Open antwoorden\\"
file_name = "nse2023_transformed.csv"
nseant_df = loaddata(path, file_name)

## Import dictionaries
# Safe words dictionaries (Dutch dictionary + whitelist)
from functions.loadSEAAdata import loaddict
word_list_df = loaddict(path=path, file_name="wordlist.txt")
whitelist_df = loaddict(path=path, file_name='whitelist.txt')
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
result_df = SEAA(nseant_df, word_list_df,flag_df, 100) # <== 4m .7s

# And save results to output file
file_name = 'SEAA_output.csv'
result_df.to_csv(f'{path}{file_name}', sep =';')

################ EXTRAS ###################
## Language detection
from langdetect import detect
def detect_language(text):
    try:
        return detect(text)
    except:
        return None
result_df['language'] = result_df['Antwoord_clean'].apply(detect_language)

## Efficiency calculation
from functions.validation import SEAA_efficiency
efficiency = SEAA_efficiency(result_df)
# Exclude English answers for efficiency calcuation
efficiency_no_en = SEAA_efficiency(result_df[result_df["language"]!='en'])

## Accuracy calculation of SEAA
validation_df = loaddata(path, "nse annoteringen totaal.csv")
from functions.validation import SEAA_accuracy
accuracy = SEAA_accuracy(validation_df, word_list_df,flag_df)

## Create list of unknown words for review
from functions.AVG_list import AVG_list
# Get list of unknown words, exclude English answers
avg_words_df = AVG_list(result_df[result_df["language"]!='en'])

# Check if word is in the flagged list
avg_words_df= avg_words_df.merge(flag_df,'left', left_on='AVG_woord',right_on='words')

# remove rows with blacklisted words and remove redundant columns
avg_words_df = avg_words_df[avg_words_df['words'].isna()].drop(columns='words')

# Save unknown words to file,
file_name = 'avg_words_count.csv'
avg_words_df.to_csv(f'{path}{file_name}', sep =';')

## Expand upon the blacklist and/or whitelist
from functions.expand_dicts import expand_dicts
whitelist_df, blacklist_df = expand_dicts(avg_words_df, whitelist_df, blacklist_df)

whitelist_df.to_csv(f'{path}//dict//whitelist.txt',index=False)
blacklist_df.to_csv(f'{path}//dict//blacklist.txt',index=False)

