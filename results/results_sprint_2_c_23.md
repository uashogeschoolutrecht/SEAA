# Pilot SEAA - 2 C 2023 (15-02-23 - 18-02-2023)

## Work done
- Added basic functions to the functions script:
    - `getAzureKey`: read secrets directly from the azure key vault
    - `readFromDB`: read directly from de MSQLoption 2
    - `readFromDBPyODBC`: read directly from de MSQLoption 2
    - `connectToSharepoint`: API connection to the HU sharepoint MDW-FCA-DA-P site
    - `readFromSharepoint`: read files directly from sharepoint folder
    - `uploadToSharePoint`: upload files directly to sharepoint folder 

Revamped the SEEA model with the following changes (functions.test_Anne):
- read the input files directly from a sharepoint folder  (with previous mentioned added funcions). 

- Added performance optimazation, instead of search in list AVG words are identified by merging. 
All words from an awnser are transformed to a dataframe and merged with the 'save' words list. NA values are marked as sensitive words. 
- Added languange detection. If an anwser contains 8 or more words and more than 40 percent of those words are unkown the awnser is classified as not Dutch and therefore can not be used in the current model.
- Revamped the `SEAA` function to make it more dynamic, added the following objects:
    - `file_path`: sharepoint site that cointains the csv file with the open awnsers folder without the organisation 
    - `open_antw_file`: csv file with the open awnsers 
    - `open_antw_col`: name of the column with open awnsers 
    - `dict_path`: sharepoint site that cointains the dict file with the open awnsers folder without the organisation 
    - `dict_file`: csv or txt file with the dict
    - `dict_col`: name of the column with
    - `testrun` object where based on the user input the length of the dataframe can be set. For testing only a certain amount of rows is needed. If testrun is set to zero (default) the model will run on the entire set

See following code snipped as example:

```python
# Run model on preselected lists
result_df = SEAA(
    # Set sharepoint file path 
    file_path=f"/sites/{specific-sharepoint-site}/{sharepointfolder}/",

    # Define file for analysis 
    open_antw_file=f"{filename}.csv",

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
```

Because not all team members are able to read from the sharepoint API a separate script is created for later use (test_Anne).
The change in the model from search in list to merge is added to the original SEAA file aswell.

## Results performance test
Total run time previous model (search in list): 6m 16.5s
Total run time new model (merge): 3m 24.7s
Results 54% runtime decrease 

## Notes 
In order to use the read from keyvault function acces to the keyvault is requiered. For members of the D&A team acces is given but for external users no acces will be given. 

## Tot Do
Additional action on what to do with non Dutch anwsers, possible sollutions:
- Skip rows 
- Add Englisch model

Alternative for keyvault acces for externals 
