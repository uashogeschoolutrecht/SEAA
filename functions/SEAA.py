def SEAA(df, df_dict):
    # Loop over answers and dictionary to find AVG sensitivity.

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
                words_in_answer = re.findall(r"(\w+)", answer)
            # Loop over individual words in answer i.
                for word in words_in_answer:
            # If the word is not in our wordlist the word may be AVG sensitive.
                    if word not in df_dict['WoordenClean'].tolist():
                        sensitive_words_amount += 1
                        sensitive_words_list += [word]
            # If no AVG sensitive words found, the answer is safe. Else, keep track which sensitive words were found.    
                if sensitive_words_amount == 0:
                    df.loc[i,'AVG_gevoelig'] = 0
                else:
                    df.loc[i,'gevoelige_woorden'] = ", ".join(sensitive_words_list)
                    print(f"Answer {i} has value {df['AVG_gevoelig'][i]}") 
                    print(sensitive_words_amount)
        except Exception as e:
            print(e)


    return df