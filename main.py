import pandas as pd
import os 
from functions.loadSEAAdata import loaddata

# import NSE open answers
logedin_user = os.getlogin()
if logedin_user == 'pim.lamberts': #User Pim does not see the parent folder
    path = f"C:\\Users\\{logedin_user}\\Stichting Hogeschool Utrecht\\FCA-DA-P - Open antwoorden\\"
else:
    path = f"C:\\Users\\{logedin_user}\\Stichting Hogeschool Utrecht\\FCA-DA-P - Analytics\\Open antwoorden\\"
file_name = "nse2023openant.csv"
nseant_df = loaddata(path, file_name)
# import Dutch word list
file_name = "wordlist.txt"
word_list_df = pd.read_csv(f"{path}{file_name}", sep =';')

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
