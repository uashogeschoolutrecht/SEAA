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
file_name = "data\\nse2023openant.csv"
nseant_df = loaddata(path, file_name)

# import Dutch word list dictionary
dictionary = "dict\\wordlist.txt"
word_list_df = loaddict(path, dictionary)

from functions.SEAA import SEAA
result_df = SEAA(nseant_df, word_list_df)

from functions.validation import SEAA_efficiency
# Calculate efficiency of SEAA
efficiency = SEAA_efficiency(result_df)

# Calculate accuracy of SEAA
validation_df = loaddata(path, "data\\nse annoteringen.csv")

from functions.validation import SEAA_accuracy
accuracy = SEAA_accuracy(validation_df, word_list_df)

#Extract AVG words with count
from AVG_list import AVG_list
avg_words_df = AVG_list(result_df)

# Save word count list to file
avg_words_df.to_csv('avg_words_count.csv', index=False) 

