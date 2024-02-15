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
    testrun=500,
)



from functions.validation import SEAA_efficiency

# Calculate efficiency of SEAA
SEAA_efficiency(result_df)

from functions.loadSEAAdata import loaddata

# Calculate accuracy of SEAA
validation_df = loaddata(path, "nse annoteringen.csv")

from functions.validation import SEAA_accuracy

SEAA_accuracy(validation_df, word_list_df)
