import os 
from functions.loadSEAAdata import loaddata
from functions.loadSEAAdata import loaddict

# import NSE open answers
logedin_user = os.getlogin()
if logedin_user == 'pim.lamberts': #User Pim does not see the parent folder
    path = f"C:\\Users\\{logedin_user}\\Stichting Hogeschool Utrecht\\FCA-DA-P - Open antwoorden\\"
else:
    path = f"C:\\Users\\{logedin_user}\\Stichting Hogeschool Utrecht\\FCA-DA-P - Analytics\\Open antwoorden\\"
file_name = "nse2023openant.csv"
nseant_df = loaddata(path, file_name)

# import Dutch word list dictionary
dictionary = "wordlist.txt"
word_list_df = loaddict(path, dictionary)

sample_df = nseant_df.head(100).reset_index(drop=True) 

from functions.loadSEAAdata import SEAA
result_df = SEAA(sample_df, word_list_df)



