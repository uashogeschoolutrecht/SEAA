import os 
import pandas as pd
from functions.loadSEAAdata import loaddata
from functions.loadSEAAdata import loaddict

# import NSE open answers
logedin_user = os.getlogin()
if logedin_user == 'pim.lamberts': #User Pim does not see the parent folder
    path = f"C:\\Users\\{logedin_user}\\Stichting Hogeschool Utrecht\\FCA-DA-P - Open antwoorden\\"
else:
    path = f"C:\\Users\\{logedin_user}\\Stichting Hogeschool Utrecht\\FCA-DA-P - Analytics\\Open antwoorden\\"
file_name = "demo.csv"
nseant_df = loaddata(path, file_name)

# import dictionaries
# Dutch word dictionary
dictionary = "wordlist.txt"
word_list_df = loaddict(path, dictionary)

# white list (words not part of the Dutch dictionary but considered safe regardless)
dictionary = 'whitelist_demo.txt'
whitelist_df = loaddict(path, dictionary)
word_list_df = pd.concat([word_list_df, whitelist_df], ignore_index=True)

# illnesses dictionary
dictionary = 'illness.txt'
illness_df = loaddict(path, dictionary, 'illness')

# Run SEAA
from functions.SEAA import SEAA
result_df = SEAA(nseant_df, word_list_df,illness_df)
result_df