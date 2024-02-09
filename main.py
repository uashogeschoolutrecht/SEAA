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
SEAA_efficiency(result_df)

# Calculate accuracy of SEAA
validation_df = loaddata(path, "data\\nse annoteringen.csv")

from functions.validation import SEAA_accuracy
SEAA_accuracy(validation_df, word_list_df)


#Retrieve list of flagged AVG words
avg_list = result_df['gevoelige_woorden'].tolist()
while('' in avg_list):
    avg_list.remove('')

avg_list_def = []
for item in avg_list:
    words = item.split(", ")
    avg_list_def.extend(words)

# Create datframe containing all AVG words with count
word_count = pd.Series(avg_list_def).value_counts()
avg_words_df = pd.DataFrame({'AVG_woord': word_count.index, 'Count': word_count.values})

csv_file_path = 'avg_words_count.csv'
avg_words_df.to_csv(csv_file_path, index=False) 