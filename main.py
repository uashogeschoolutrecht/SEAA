# run the main functions
import pandas as pd
import os 

# import NSE open answers
logedin_user = os.getlogin()
path = f"C:\\Users\\{logedin_user}\\Stichting Hogeschool Utrecht\\FCA-DA-P - Open antwoorden\\"
file_name = "nse2023openant.csv"
nseant_df = pd.read_csv(f'{path}{file_name}', sep =';')

# import Dutch word list
file_name = "Opentaal_woordenlijst.txt"
word_list_df = pd.read_csv(f"{path}{file_name}", sep =';')

# Quick data check. What are we working with.
# print(nseant_df['Antwoord'][50])
# print(word_list_df['WoordenLijst'][50])
# print(type(nseant_df))

# Expand NSE open answers. Add columns for AVG sensitivity and AVG sensitive words.
## AVG sensitivity is either 0 or 1. preset 0 is not sensitive.
nseant_df['AVG_gevoelig'] = 0
## Column to print words in answers but not in imported dictionary
# nseant_df['gevoelige_woorden'] = ''

# Loop over NSE answers and word list to find AVG sensitive words in answers.
gevoelige_woorden = 0

for i in range(1,10):
    for word in word_list_df['WoordenLijst']:
        if nseant_df['Antwoord'][i] not in word_list_df['WoordenLijst']:
            gevoelige_woorden += 1
    if gevoelige_woorden >= 1:
        nseant_df['AVG_gevoelig'][i] = 1
        print(f"Answer {i} has value {nseant_df['AVG_gevoelig'][i]}")   
           
     
