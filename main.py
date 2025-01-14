import os
import pandas as pd
from functions.loadSEAAdata import loaddata, loaddict
from functions.nse.transform_raw_data import transform_nse_data
from functions.SEAA import SEAA
# from langdetect import detect
from functions.AVG_list import AVG_list
from functions.expand_dicts import expand_dicts


# def detect_language(text):
#     try:
#         return detect(text)
#     except:
#         return None

def main(path, file_name, input_file_name=None):
    
    
    # If NSE transform raw data
    if input_file_name is not None:
        transform_nse_data(
            input_path=path,
            input_file_name=input_file_name,
        )
        file_name='nse_transformed.csv'
    
    nseant_df = loaddata(path, file_name)

    # Import dictionaries
    word_list_df = loaddict(file_name="wordlist.txt", type='known')
    whitelist_df = loaddict(file_name='whitelist_demo.txt')
    word_list_df = pd.concat([word_list_df, whitelist_df], ignore_index=True)

    # Flag words
    flag_df = pd.DataFrame()
    for file_name,file_type in [('illness.txt', 'illness'), ('studiebeperking.txt', 'disability'), ('firstnames.txt', 'name'), ('blacklist.txt', 'blacklist')]:
        temp_df = loaddict(file_name=file_name, type=file_type)
        flag_df = pd.concat([flag_df, temp_df], ignore_index=True)
    del temp_df

    df_dict = word_list_df
    df_flag = flag_df
    df = nseant_df
    
    N = 122
    
    # Run SEAA
    '''Semi-automatic anonimisation algorithm

    Input is 3 dataframes:
    - a dataframe df containing text to be checked by SEAA
    for possible privacy-related data in the column ['answer_clean']
    - a dataframe df_dict: a list of words that are considered safe,
    i.e. not privacy-related. 
    - a dataframe df_flag: a list of words that are considered unsafe,
    i.e. containing privacy-related information. 
    - integer N (optional), number of answers to check (usefull for testing)

    Output is dataframe df with one extra column ['contains_privacy'] 
    indicating whether the column might contain privacy-related data (1)
    or not does not (0). '''

    import re
    import pandas as pd

    df_dict["known"] = 1
    df_flag["known"] = 1
    df["answer_censored"] = ""
    df["total_word_count"] = 0
    df["unknown_word_count"] = 0
    df["flagged_word_count"] = 0

    # Set col_name for merge, making sure that both columns have the same name
    col_name = df_dict.columns[0]

    # Loop over all rows of answers
    for i in df.index:
        answer = df["answer_clean"][i]
        try:
            # If answer contains no value, set output
            if pd.isna(df["answer_clean"][i]):
                df.loc[i, "contains_privacy"] = 0
            # Else continue with SEAA
            else:
                answer_df = pd.DataFrame({col_name: re.findall(r"(\w+)", answer)})
                check_df = pd.merge(answer_df, df_dict, "left")

                # Count the number of words in the answer
                words_number = len(check_df[col_name])
                df.loc[i, "total_word_count"] = words_number

                # Find number of unknown words
                unknown_words_number = int(words_number - check_df["known"].sum())  
                    
                # Select list of unknown words
                unknown_words_list = check_df[check_df["known"].isnull()][
                    col_name
                ].tolist()
                
                # If at least one word is unknown, 'contains_privacy' is set to 1
                if unknown_words_number >= 1:                    
                    df.loc[i, "contains_privacy"] = 1
                    df.loc[i, "unknown_words"] = ", ".join(unknown_words_list)
                    
                    # for unknown words add column with amount of unknown words plus total number of words 
                    df.loc[i, "unknown_word_count"] = unknown_words_number                        
                    
                    print(
                        f"Answer {i} might contain privacy-related data: {unknown_words_number} unknown word(s)."
                    )
                # If case does not contain unknown words 'contains_privacy' is set to 0
                else:
                    df.loc[i, "contains_privacy"] = 0

                # Repeat for flagged words
                check_df = pd.merge(answer_df, df_flag, "left")

                # If looking for flagged words take the sum of the total known
                flagged_words_number = int(check_df["known"].sum())
                if flagged_words_number >= 1:
                    flagged_words_list = check_df[~check_df["known"].isnull()][
                        col_name
                    ].tolist()
                    df.loc[i,'flagged_words'] = ", ".join(flagged_words_list)
                    df.loc[i, "contains_privacy"] = 1         
                    print(f"Answer {i} contains privacy-related data: {flagged_words_number} flagged word(s).")                                                                             

                    df.loc[i, "flagged_word_count"] = flagged_words_number       

                    # Censor flagged words
                    mask = check_df['known'] == 1
                    check_df.loc[mask, 'words'] = "XXX"
                    
                df.loc[i, "answer_censored"] = ' '.join(check_df["words"])
        except Exception as e:
            print(e)    
        # Exit the loop early for testing purposes
        if i == N:
            break
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    result_df = SEAA(nseant_df, word_list_df, flag_df)

    # Save results to output file
    file_name = 'SEAA_output.csv'
    result_df.to_csv(f'{path}{file_name}', sep=';')

    # Language detection
    result_df['language'] = result_df['answer_clean'].apply(detect_language)

    # Create list of unknown words for review
    avg_words_df = AVG_list(result_df[result_df["language"] != 'en'])
    avg_words_df = avg_words_df.merge(flag_df, 'left', left_on='AVG_woord', right_on='words')
    avg_words_df = avg_words_df[avg_words_df['words'].isna()].drop(columns='words')

    # Save unknown words to file
    file_name = 'avg_words_count.csv'
    avg_words_df.to_csv(f'{path}{file_name}', sep=';')

    # Expand upon the blacklist and/or whitelist
    whitelist_df, blacklist_df = expand_dicts(avg_words_df, whitelist_df, blacklist_df)

    # Save lists to file
    whitelist_df.to_csv(f'{path}//dict//whitelist.txt', index=False)
    blacklist_df.to_csv(f'{path}//dict//blacklist.txt', index=False)


if __name__ == "__main__":
    # SET THE PATH AND FILE NAME
    path = r'C:\Users\AnneL\OneDrive - Stichting Hogeschool Utrecht\Documents\testpath'
    input_file_name = "nse2023.csv"
    main(path, file_name)



