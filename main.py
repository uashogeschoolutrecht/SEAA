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

from functions.SEAA import SEAA
result_df = SEAA(nseant_df, word_list_df)

from functions.validation import SEAA_efficiency
# Calculate efficiency of SEAA
SEAA_efficiency(result_df)

# Calculate accuracy of SEAA
validation_df = loaddata(path, "nse annoteringen.csv")

from functions.validation import SEAA_accuracy
SEAA_accuracy(validation_df, word_list_df)

# Create a list of all 'gevoelige woorden'
col_avg_list = result_df['gevoelige_woorden'].tolist()
col_avg_list = [i for i in col_avg_list if i]
avg_list = [sub_item for item in col_avg_list for sub_item in item.split(", ")]
unique_avg_list = []

# Keep unique 'gevoelige woorden'
# Improvement: add count per unique value
for word in avg_list:
    if word not in unique_avg_list:
        unique_avg_list.append(word)

# Write list to csv file
import csv
csv_file_path = 'unique_avg_words.csv'

with open(csv_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    for item in unique_avg_list:
        csv_writer.writerow([item])


