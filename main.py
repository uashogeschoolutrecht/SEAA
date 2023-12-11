# run the main functions
import pandas as pd
import os 

# import NSE open answers
logedin_user = os.getlogin()
if logedin_user == 'pim.lamberts': #User Pim does not see the parent folder
    path = f"C:\\Users\\{logedin_user}\\Stichting Hogeschool Utrecht\\FCA-DA-P - Open antwoorden\\"
else:
    path = f"C:\\Users\\{logedin_user}\\Stichting Hogeschool Utrecht\\FCA-DA-P - Analytics\\Open antwoorden\\"
file_name = "nse2023openant.csv"
nseant_df = pd.read_csv(f'{path}{file_name}', sep =';')

# import Dutch word list
file_name = "wordlist.txt"
word_list_df = pd.read_csv(f"{path}{file_name}", sep =';')

# Add columns: 1 for AVG sensitivity and 1 to track AVG sensitive words.
## AVG sensitivity is either 0 or 1. preset 1 means sensitive.
nseant_df['AVG_gevoelig'] = 1
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
    answer = sample_df['Antwoord_clean'][i]
    sensitive_words_amount = 0                             
    sensitive_words_list = []                            
    words_in_answer = re.findall(r"(\w+)", answer)
# Loop over individual words in answer i.
    for word in words_in_answer:
# If the word is not in our wordlist the word may be AVG sensitive.
        if word not in word_list_df['WoordenClean'].tolist():
            sensitive_words_amount += 1
            sensitive_words_list += [word]
# If no AVG sensitive words found, the answer is safe. Else, keep track which sensitive words were found.    
    if sensitive_words_amount == 0:
        sample_df.loc[i,'AVG_gevoelig'] = 0
    else:
        sample_df.loc[i,'gevoelige_woorden'] = ", ".join(sensitive_words_list)
        print(f"Answer {i} has value {sample_df['AVG_gevoelig'][i]}") 
        print(sensitive_words_amount)
