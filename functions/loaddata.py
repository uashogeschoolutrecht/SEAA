import pandas as pd
import os
import nltk
import numpy as np
import re

# Import data
logedin_user = os.getlogin()
path = f"C:\\Users\\{logedin_user}\\Stichting Hogeschool Utrecht\\FCA-DA-P - Analytics\\Open antwoorden\\"
file_name = "nse2023openant.csv"
df = pd.read_csv(f'{path}{file_name}', sep =';')

# Import dictionary of Dutch words
words = pd.read_csv(r'files\wordlist.txt', sep = ';')
words['AVG'] = 0

# Clean both dataframes (data + dictionary)
df['antwoord_clean'] = df['Antwoord'].str.lower() 
words['WoordenClean'] = words['WoordenClean'].str.lower() 
words = words.drop_duplicates()
words.reset_index(inplace=True,drop=True)

# Remove null values
df = df[~df['antwoord_clean'].isnull()]

# For each string, determine whether it is contains privacy-related (AVG) data.
df['AVG'] = 0
for i in range(1,100):
    test = df['antwoord_clean'][i]
    test_df = pd.DataFrame({'WoordenClean':re.findall(r'(\w+)', test)})
    check_df = pd.merge(test_df,words,'left')
    check_df['AVG'] = np.where(check_df['AVG'].isnull(),1,0)

    if check_df['AVG'].sum() >= 1:
        df.loc[i,'AVG'] = 1
    else:
        df.loc[i,'AVG'] = 0
    print(f'{round(i/1000*100,0)}%')

print('done')

