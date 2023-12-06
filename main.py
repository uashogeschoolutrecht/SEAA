# run the main functions
import pandas as pd
import os 

# import NSE open answers
logedin_user = os.getlogin()
path = f"C:\\Users\\{logedin_user}\\Stichting Hogeschool Utrecht\\FCA-DA-P - Open antwoorden\\"
file_name = "nse2023openant.csv"
nseant_df = pd.read_csv(f'{path}{file_name}', sep =';')

# import Dutch word list
file_name = "wordlist.txt"
word_list_df = pd.read_csv(f"{path}{file_name}", sep =';')

# Add columns: 1 for AVG sensitivity and 1 for AVG sensitive words.
## AVG sensitivity is either 0 or 1. preset 0 is not sensitive.
nseant_df['AVG_gevoelig'] = 0
## Column to print words present in answers but not in imported dictionary.
nseant_df['gevoelige_woorden'] = ''

import re
# Answers in lower case and remove numbers.
nseant_df['Antwoord_clean'] = nseant_df['Antwoord'].str.lower()
nseant_df['Antwoord_clean'] = nseant_df['Antwoord_clean'].str.replace(r"([0-9])", "", regex=True)

sample_df = nseant_df.head(100).reset_index(drop=True) 
# Loop over NSE answers and word list to find AVG sensitivity.
# Start loop over NSE answers.
for i in sample_df.index:
    antwoord = sample_df['Antwoord_clean'][i]
    gevoelige_woorden_aantal = 0                             
    gevoelige_woorden_lijst = []                            
    antwoord_woorden = re.findall(r"(\w+)", antwoord)
# Loop over individual words in answer i.
    for woord in antwoord_woorden:
# If the word is not in our wordlist the word may be AVG sensitive.
        if woord not in word_list_df['WoordenClean'].tolist():
            gevoelige_woorden_aantal += 1
            gevoelige_woorden_lijst += [woord]
# If AVG sensitive words have been found, keep tally and which words.    
    if gevoelige_woorden_aantal >= 1:
        sample_df.loc[i,'AVG_gevoelig'] = 1
        sample_df.loc[i,'gevoelige_woorden'] = ", ".join(gevoelige_woorden_lijst)
        print(f"Answer {i} has value {sample_df['AVG_gevoelig'][i]}") 
        print(gevoelige_woorden_aantal)
