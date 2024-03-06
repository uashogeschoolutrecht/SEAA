def SEAA(df, df_dict, df_flag, N=-1):
    '''Semi-automatic anonimisation algorithm
    
    Input is 2 dataframes:
    - a dataframe df containing text to be checked by SEAA
    for possible privacy-related data in the column ['Antwoord_clean']
    - a dataframe df_dict: a list of words that are considered safe,
    i.e. not privacy-related. 
    - a dataframe df_flag: a list of words that are considered unsafe,
    i.e. containing privacy-related information. 
    - integer N (optional), number of answers to check (usefull for testing)
    
    Output is dataframe df with one extra column ['AVG_gevoelig'] 
    indicating whether the column might contain privacy-related data (1)
    or not does not (0). '''

    import re
    import pandas as pd
    df_dict["known"] = 1
    df_flag["known"] = 1
    for i in df.index:
        test = df["Antwoord_clean"][i]
        try:
            if pd.isna(df["Antwoord_clean"][i]):
                df.loc[i, "AVG_gevoelig"] = 0
                df.loc[i, "NL/NietNL"] = "NL"
            else:
                for df2,dict_type in zip([df_dict,df_flag],['sensitive','flagged']):
                    # Set col_name for merge, making sure that both columns have the same name
                    col_name = df2.columns[0]
                    test_df = pd.DataFrame({col_name: re.findall(r"(\w+)", test)})
                    check_df = pd.merge(test_df, df2, "left")

                    # Count te number of words in the awnser
                    words_amount = len(check_df[col_name])

                    # If looking for sensitive words. Amount of unknow words based on total words minus known words
                    if dict_type == 'sensitive':
                        forbidden_words_amount = words_amount - check_df["known"].sum()      
                        # Select list of sensitive words
                        sensitive_words_list = check_df[check_df["known"].isnull()][
                            "words"
                        ].tolist()
                        
                        if forbidden_words_amount >= 1:                    
                            df.loc[i, "AVG_gevoelig"] = 1
                            df.loc[i, "gevoelige_woorden"] = ", ".join(sensitive_words_list)
                            
                            # for sensitive words add column with amount of sensitive words plus amount of words 
                            # this is for later langauage analysis.
                            df.loc[i, "total_word_count"] = words_amount
                            df.loc[i, "sensitive_word_count"] = forbidden_words_amount                        
                            
                            print(
                                f"Answer {i} might contain privacy-related data: {forbidden_words_amount} unknown word(s)."
                            )
                        # If no unknown words are found AVG is set to 0
                        else:
                            df.loc[i, "AVG_gevoelig"] = 0
                    else:
                        # If looking for flagged words take the sum of the total known
                        forbidden_words_amount = check_df["known"].sum()
                        if forbidden_words_amount >= 1:
                            flagged_words_list = check_df[~check_df["known"].isnull()][
                                "words"
                            ].tolist()
                            df.loc[i,'flagged words'] = ", ".join(flagged_words_list)
                            df.loc[i, "AVG_gevoelig"] = 1         
                            print(f"Answer {i} contains privacy-related data: {forbidden_words_amount} illness word(s).")                                                                             
        except Exception as e:
            print(e)
        # Exit the loop early for testing purposes
        if i == N:
            break

    return df

        
        
        
                
                
