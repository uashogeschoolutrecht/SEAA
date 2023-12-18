## Input is DF with at least the following columns:
# 1. AVG: classification of SEAA algorithm on whether row has AVG data = 1 or 0, 
# 2. actual__AVG = 1 or 0 (whether column actually has AVG data)
# efficiency --> number of detected cases without AVG / total cases
# accuracy   --> number of correctly detected cases / total cases

def SEAA_efficiency(df):
    '''df = dataframe with column ['AVG_gevoelig'] that contains classification of SEAA 
    algorithm whether row has AVG data (1) or not (0). '''

    # Calculate efficiency (%)
    efficiency = (1 - (sum(df['AVG_gevoelig']) / len(df)))*100

    return efficiency

def SEAA_accuracy(df, df_dict):
    '''Calculate accuracy of SEAA algorithm based on validation data''' 

    #Run SEAA on validation data
    from functions.SEAA import SEAA
    result_df = SEAA(df, df_dict)
    
    # Calculate accuracy
    # When AVG_gevoelig is 1, it means that SEAA  determined the string to be containing 
    # AVG data. 
    # This is true when the actual string did contain any privacy-related 
    # fields (AVG validatie = 1).
    # When AVG_gevoelig is 0, SEAA determined that the string is AVG-free, so it will not
    # contain AVG data (AVG validatie = 0).
    #
    # When assessing the algorithm SEAA the output of SEAA for a case falls 
    # into one of the following four categories:
    # True positive: AVG_gevoelig = 1 and AVG validatie = 1
    # True negative: AVG_gevoelig = 0 and AVG validatie = 0
    # False positive: AVG_gevoelig = 1 and AVG validatie = 0
    # False negative = AVG_gevoelig = 0 and AVG validatie = 1
    #
    # Accuracy = (true positives + true negatieve) / total cases
    true_positives = sum((result_df['AVG validatie']==1) & (result_df['AVG_gevoelig'] == 1));
    true_negatives = sum((result_df['AVG validatie']==0) & (result_df['AVG_gevoelig'] == 0));
    accuracy = (true_positives + true_negatives) / len(result_df) * 100

    return accuracy
