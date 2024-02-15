def SEAA(file_path, open_antw_file, open_antw_col, dict_path, dict_file, dict_col, testrun=0):
    """Semi-automatic anonimisation algorithm

    Input is 2 dataframes:
    - a dataframe df containing text to be checked by SEAA
    for possible privacy-related data in the column ['Antwoord_clean']
    - a dataframe df_dict: a list of words that are considered safe,
    i.e. not privacy-related.
    - integer N (optional), number of answers to check (usefull for testing)

    Output is dataframe df with one extra column ['AVG_gevoelig']
    indicating whether the column might contain privacy-related data (1)
    or not does not (0)."""

    ### Load analyse data
    from functions.functions import getAzureKey
    from functions.functions import connectToSharepoint
    from functions.functions import readFromSharepoint
    from functions.loadSEAAdata import loaddataNew

    ## Connect to sharepoint
    ctx = connectToSharepoint(
        client_id=getAzureKey("KV-DENA", "KVK-SPK-SHA-PROD").split("@")[0],
        client_secret=getAzureKey("KV-DENA", "KVS-SPK-SHA-PROD"),
    )

    ## Get file from sharepoint folder
    shp_response = readFromSharepoint(
        ctx=ctx,
        shp_folder=file_path,
        shp_file_name=open_antw_file,
    )

    ## Load file to pandas dataframe
    df = loaddataNew(shp_response, open_antw_col)

    ## Set test length
    if testrun > 0:
        df = df.head(testrun)
    else:
        df = df

    ## Get dicts
    shp_response = readFromSharepoint(
        ctx=ctx,
        shp_folder=dict_path,
        shp_file_name=dict_file,
    )

    import io
    import pandas as pd
    import re

    ## SHP object to dataframe
    word_list_df = pd.read_csv(io.BytesIO(shp_response.content), sep=";")

    # add identifier to wordlist for
    word_list_df["known"] = 1
    for i in df.index:
        test = df["Antwoord_clean"][i]
        if pd.isna(test):
            df.loc[i, "AVG_gevoelig"] = 0
            df.loc[i, "NL/NietNL"] = "NL"
        else:
            # Set col_name for merge, making sure that both columns are have the same name
            col_name = word_list_df.columns[0]
            test_df = pd.DataFrame({col_name: re.findall(r"(\w+)", test)})
            check_df = pd.merge(test_df, word_list_df, "left")

            # Count te number of words in the awnser
            words_amount = len(check_df[dict_col])

            # Amount of unknow words based on total words minus known words
            sensitive_words_amount = words_amount - check_df["known"].sum()

            # Calculate precentage unknown and add to dataframe
            # skip rows with less than 8 awnsers (not enough info for analysis)
            if words_amount >= 8:
                percentage_unknown = round(sensitive_words_amount / words_amount, 2)
            else:
                percentage_unknown = 0

            # Add Dutch or not Dutch column classificatiion
            # If the anwser contains 8 or more words and more than 40 percent of those words are unkown
            # the awnser will be classified as not Dutch

            if percentage_unknown > 0.4:
                df.loc[i, "NL/NietNL"] = "Niet NL"
            else:
                df.loc[i, "NL/NietNL"] = "NL"

            # Select list of sensitive words
            sensitive_words_list = check_df[check_df["known"].isnull()][
                dict_col
            ].tolist()

            if sensitive_words_amount >= 1:
                df.loc[i, "AVG_gevoelig"] = 1
                df.loc[i, "gevoelige_woorden"] = ", ".join(sensitive_words_list)
                print(
                    f"Answer {i} might contain privacy-related data: {sensitive_words_amount} unknown word(s)."
                )
            else:
                df.loc[i, "AVG_gevoelig"] = 0
    return df
