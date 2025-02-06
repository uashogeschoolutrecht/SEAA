import re
import pandas as pd
from flask import current_app

def SEAA(df, dictionary_df, flag_df, limit=-1):
    """Semi-automatic anonymization algorithm
    
    Args:
        dataframe: DataFrame containing text to check in column ['answer_clean']
        dictionary_df: DataFrame of safe words (not privacy-related)
        flag_df: DataFrame of unsafe words (privacy-related)
        limit: Optional integer, number of answers to check (useful for testing)
    
    Returns:
        DataFrame with additional columns including 'contains_privacy' flag
    """
    
    dataframe = df.copy()
    # set if limit is set
    if limit > 0:
        dataframe = dataframe.head(limit)

    # Initialize flags in dictionary and flag dataframes
    dictionary_df["is_known"] = 1
    flag_df["is_known"] = 1

    # Initialize new columns in main dataframe
    dataframe["answer_censored"] = ""
    dataframe["total_word_count"] = 0
    dataframe["unknown_word_count"] = 0
    dataframe["flagged_word_count"] = 0
    dataframe["unknown_words_not_flagged"] = ""
    # Use consistent column name for merging
    word_column = dictionary_df.columns[0]

    # Get total number of rows
    total_rows = len(dataframe.index)

    # Process each answer
    for current_idx, idx in enumerate(dataframe.index):
        answer = dataframe["answer_clean"][idx]
        try:
            if pd.isna(answer):
                dataframe.loc[idx, "contains_privacy"] = 0
                dataframe.loc[idx, "answer_censored"] = answer
                
                # Calculate and emit progress
                progress = (current_idx + 1) / total_rows * 100
                if hasattr(current_app, 'progress_queue'):
                    current_app.progress_queue.put(progress)
                    
                continue
            
            # Initialize unknown words not flagged
            unknown_words_not_flagged = []
            unknown_words_list = []
            flagged_words_list = []
            answer_censored = answer 
            
            
            # Create DataFrame of words from answer
            words_df = pd.DataFrame({word_column: re.findall(r"(\w+)", answer)})
            
            # Check against dictionary
            unknown_check = pd.merge(words_df, dictionary_df, "left")
            total_words = len(unknown_check[word_column])
            dataframe.loc[idx, "total_word_count"] = total_words

            # Process unknown words
            unknown_count = int(total_words - unknown_check["is_known"].sum())
            if unknown_count >= 1:
                unknown_words_list = unknown_check[unknown_check["is_known"].isnull()][word_column].tolist()
                dataframe.loc[idx, "contains_privacy"] = 1
                dataframe.loc[idx, "unknown_words"] = ", ".join(unknown_words_list)
                dataframe.loc[idx, "unknown_word_count"] = unknown_count
                print(f"Answer {idx} might contain privacy-related data: {unknown_count} unknown word(s).")
            else:
                dataframe.loc[idx, "contains_privacy"] = 0

            # Check against flag list
            flag_check = pd.merge(words_df, flag_df, "left")
            flagged_count = int(flag_check["is_known"].sum())
            
            if flagged_count >= 1:
                flagged_words_list = flag_check[~flag_check["is_known"].isnull()][word_column].tolist()
                dataframe.loc[idx, "contains_privacy"] = 1
                dataframe.loc[idx, "flagged_word_count"] = flagged_count
                flag_type = flag_check[~flag_check["is_known"].isnull()]['dict_type'].tolist()
                dataframe.loc[idx, "flagged_word_type"] = ", ".join(flag_type)
                print(f"Answer {idx} contains privacy-related data: {flagged_count} flagged word(s).")      
            else:        
                flagged_words_list = []
            
            dataframe.loc[idx, "flagged_words"] = ", ".join(flagged_words_list)
        
            if flagged_count == 0 and unknown_count == 0:
                unknown_words_not_flagged = []
            elif flagged_count == 0 and unknown_count > 0:
                unknown_words_not_flagged = unknown_words_list.copy()
            else:        
                # Censor flagged words and unknown words
                # New column that shows all unknown words that are not flagged
                for unknown_word in unknown_words_list:
                    if unknown_word not in flagged_words_list:
                        unknown_words_not_flagged.append(unknown_word)
                    
            # Add to dataframe
            dataframe.loc[idx, "unknown_words_not_flagged"] = ", ".join(unknown_words_not_flagged)      

            # Censor flagged words
            if len(flagged_words_list) > 0:
                for flagged_word,flag_type in zip(flagged_words_list,flag_type):
                    answer_censored = re.sub(flagged_word,f'[{flag_type.upper()}]',answer_censored)
                    
            # Censor unknown words not flagged
            if len(unknown_words_not_flagged) > 0:
                for unknown_words_not_flagged in unknown_words_not_flagged:
                    answer_censored = re.sub(unknown_words_not_flagged,f'[UNKNOWN]',answer_censored)
                                            
            # Add to dataframe
            dataframe.loc[idx, "answer_censored"] = answer_censored

            # Add progress update at the end of each iteration
            progress = (current_idx + 1) / total_rows * 100
            if hasattr(current_app, 'progress_queue'):
                current_app.progress_queue.put(progress)

        except Exception as e:
            print(f"Error processing row {idx}: {str(e)}")  
         

            

    return dataframe

        
        
        
                
                
