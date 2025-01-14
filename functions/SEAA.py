def semi_automatic_anonymization(dataframe, dictionary_df, flag_df, limit=-1):
    """Semi-automatic anonymization algorithm
    
    Args:
        dataframe: DataFrame containing text to check in column ['answer_clean']
        dictionary_df: DataFrame of safe words (not privacy-related)
        flag_df: DataFrame of unsafe words (privacy-related)
        limit: Optional integer, number of answers to check (useful for testing)
    
    Returns:
        DataFrame with additional columns including 'contains_privacy' flag
    """

    import re
    import pandas as pd

    # Initialize flags in dictionary and flag dataframes
    dictionary_df["is_known"] = 1
    flag_df["is_known"] = 1
    
    # Initialize new columns in main dataframe
    dataframe["answer_censored"] = ""
    dataframe["total_word_count"] = 0
    dataframe["unknown_word_count"] = 0
    dataframe["flagged_word_count"] = 0

    # Use consistent column name for merging
    word_column = dictionary_df.columns[0]

    # Process each answer
    for idx in dataframe.index:
        answer = dataframe["answer_clean"][idx]
        try:
            if pd.isna(answer):
                dataframe.loc[idx, "contains_privacy"] = 0
                continue

            # Create DataFrame of words from answer
            words_df = pd.DataFrame({word_column: re.findall(r"(\w+)", answer)})
            
            # Check against dictionary
            unknown_check = pd.merge(words_df, dictionary_df, "left")
            total_words = len(unknown_check[word_column])
            dataframe.loc[idx, "total_word_count"] = total_words

            # Process unknown words
            unknown_count = int(total_words - unknown_check["is_known"].sum())
            if unknown_count >= 1:
                unknown_words = unknown_check[unknown_check["is_known"].isnull()][word_column].tolist()
                dataframe.loc[idx, "contains_privacy"] = 1
                dataframe.loc[idx, "unknown_words"] = ", ".join(unknown_words)
                dataframe.loc[idx, "unknown_word_count"] = unknown_count
                print(f"Answer {idx} might contain privacy-related data: {unknown_count} unknown word(s).")
            else:
                dataframe.loc[idx, "contains_privacy"] = 0

            # Check against flag list
            flag_check = pd.merge(words_df, flag_df, "left")
            flagged_count = int(flag_check["is_known"].sum())
            
            if flagged_count >= 1:
                flagged_words = flag_check[~flag_check["is_known"].isnull()][word_column].tolist()
                dataframe.loc[idx, "flagged_words"] = ", ".join(flagged_words)
                dataframe.loc[idx, "contains_privacy"] = 1
                dataframe.loc[idx, "flagged_word_count"] = flagged_count
                print(f"Answer {idx} contains privacy-related data: {flagged_count} flagged word(s).")

                # Censor flagged words
                mask = flag_check["is_known"] == 1
                flag_check.loc[mask, "words"] = "XXX"
                
            dataframe.loc[idx, "answer_censored"] = " ".join(flag_check["words"])

        except Exception as e:
            print(f"Error processing row {idx}: {str(e)}")
            
        if idx == limit:
            break

    return dataframe

        
        
        
                
                
