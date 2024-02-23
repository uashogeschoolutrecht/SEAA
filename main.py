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
file_name = "nse2023openant.csv"
nseant_df = loaddata(path, file_name)

# import dictionaries
# Dutch word dictionary
dictionary = "wordlist.txt"
word_list_df = loaddict(path, dictionary)

# white list (words not part of the Dutch dictionary but considered safe regardless)
dictionary = 'whitelist.txt'
whitelist_df = loaddict(path, dictionary)
word_list_df = pd.concat([word_list_df, whitelist_df], ignore_index=True)

# illnesses dictionary
dictionary = 'illness.txt'
illness_df = loaddict(path, dictionary, 'illness')

# Run SEAA
from functions.SEAA import SEAA
result_df = SEAA(nseant_df, word_list_df,illness_df)


# Run SEAA Max Performance 

from functions.SEAA_performance import SEAA

# Run model on preselected lists
result_df = SEAA(
    # Set sharepoint file path 
    file_path="/sites/MDW-FCA-DA-P/Analytics/Open antwoorden/data/",

    # Define file for analysis 
    open_antw_file="nse2023openant.csv",

    # Define Column name 
    open_antw_col="Antwoord",

    # Set sharepoint dict path
    dict_path="/sites/MDW-FCA-DA-P/Analytics/Open antwoorden/dict/",

    # Define Dict
    dict_file="wordlist.txt",

    # Define Dict column
    dict_col="words",

    # Define numer of lines for test run !NOTE set to 0 for a FULL run
    testrun=0,
)

from functions.validation import SEAA_efficiency
# Calculate efficiency of SEAA
efficiency = SEAA_efficiency(result_df)

# Calculate accuracy of SEAA
validation_df = loaddata(path, "nse annoteringen.csv")

from functions.validation import SEAA_accuracy
accuracy = SEAA_accuracy(validation_df, word_list_df, illness_df)

#Extract AVG words with count
from AVG_list import AVG_list
avg_words_df = AVG_list(result_df)

# Save word count list to file
file_name = 'avg_words_count.csv'
avg_words_df.to_csv(f'{path}{file_name}', sep =';')




from functions.validation import SEAA_efficiency

# Calculate efficiency of SEAA
SEAA_efficiency(result_df)

from functions.loadSEAAdata import loaddata

# Calculate accuracy of SEAA
validation_df = loaddata(path, "nse annoteringen.csv")

from functions.validation import SEAA_accuracy

SEAA_accuracy(validation_df, word_list_df)
