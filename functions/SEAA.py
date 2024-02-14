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
    from functions.loadSEAAdata import loaddict

    # Start loop over  answers.
    for i in df.index:
        try:
            answer = df['Antwoord_clean'][i]
            if pd.isna(answer):
                df.loc[i,'AVG_gevoelig'] = 0
                #skip NaN answer
            else:
                sensitive_words_amount = 0                             
                sensitive_words_list = []       
                flagged_words_number = 0
                flagged_words_list = []                     
                words_in_answer = re.findall(r"(\w+)", answer)
            # Loop over individual words in answer i.
                for word in words_in_answer:
            # If the word is not in our wordlist the word may be AVG sensitive.
                    if word not in df_dict['WoordenClean'].tolist():
                        sensitive_words_amount += 1
                        sensitive_words_list += [word]
            # If the word is an illness word, flag the word
                    if word in df_flag['Illness'].tolist():
                        flagged_words_number += 1
                        flagged_words_list += [word]
            # If no AVG sensitive words found, the answer is safe. Else, keep track which sensitive words were found.    
                if sensitive_words_amount  == 0 & flagged_words_number == 0:
                    df.loc[i,'AVG_gevoelig'] = 0
                elif flagged_words_number > 0:
                    df.loc[i,'flagged words'] = ", ".join(flagged_words_list)
                    df.loc[i,'gevoelige_woorden'] = ", ".join(sensitive_words_list)
                    print(f"Answer {i} contains privacy-related data: {flagged_words_number} illness word(s).") 
                else:
                    df.loc[i,'gevoelige_woorden'] = ", ".join(sensitive_words_list)
                    print(f"Answer {i} might contain privacy-related data: {sensitive_words_amount} unknown word(s).") 
        except Exception as e:
            print(e)
        # Exit the loop early for testing purposes
        if i == N:
            break

    return df