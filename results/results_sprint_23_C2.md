# Pilot SEAA - 2 C 2023 (15-02-23 - 18-02-2023)

## Work done
Added read directly from sharepoint through sharepoint API. Credentials are fetched from the DENA keyvault with a getkeys function (added to the functions script). 
Assed performance optimazation, instead of search in list AVG words are identified by merging. All words from an awnser are transformed to a dataframe and merged with the 'save' words list. NA values are marked as sensitive words. 

## Results performance test
Total run time previous model (search in list): 6m 16.5s
Total run time new model (merge): 3m 24.7s
Results 54% runtime decrease 

## Notes 
In order to use the read from keyvault function acces to the keyvault is requiered. For members of the D&A team acces is given but for external users no acces will be given. 

## Additional changes
Added languange detection. If an anwser contains 8 or more words and more than 40 percent of those words are unkown the awnser is classified as not Dutch and therefore can not be used in the current model.

## Tot Do
Additional action on what to do with non Dutch anwsers, possible sollutions:
- Skip rows
- Add Englisch model
- Alternative for keyvault acces for externals 
