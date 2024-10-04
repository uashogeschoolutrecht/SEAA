def SEAA_efficiency(df):
    '''Calculate efficiency of SEAA algorithm: the number of detected cases
    without privacy-related data with respect to the total number of cases. 
    INPUT:
    df = dataframe with column ['Contains privacy'] that contains classification of SEAA 
    algorithm whether row has AVG data (1) or not (0). '''

    # Calculate efficiency (%)
    efficiency = (1 - (sum(df['Contains privacy']) / len(df)))*100

    return efficiency

def SEAA_accuracy(df, df_dict, df_flag):
    '''Calculate accuracy of SEAA algorithm based on annotated data.
    
    When Contains privacy is 1, it means that SEAA  determined the string to 
    be containing privacy-related data. 
    This is true when the actual string did contain any privacy-related 
    fields (AVG validatie = 1), i.e. a true positive. When Contains privacy 
    is 0, SEAA determined that the string is AVG-free, so it will not
    contain AVG data (AVG validatie = 0).
    
    When assessing the algorithm SEAA the output of SEAA for a case falls 
    into one of the following four categories:
    - True positive: Contains privacy = 1 and AVG validatie = 1
    - True negative: Contains privacy = 0 and AVG validatie = 0
    - False positive: Contains privacy = 1 and AVG validatie = 0
    - False negative = Contains privacy = 0 and AVG validatie = 1''' 

    #Run SEAA on annotated data
    from functions.SEAA import SEAA
    result_df = SEAA(df, df_dict, df_flag)
    
    # Calculate accuracy
    # We define accuracy as the proporition of correctly classified cases (true positives) 
    # with respect to the total number of cases that contain privacy-related data (AVG 
    # validatie = 1, i.e. true posities + false negatives).
    true_positives = sum((result_df['AVG validatie']==1) & (result_df['Contains privacy'] == 1));
    false_negatives = sum((result_df['AVG validatie']==1) & (result_df['Contains privacy'] == 0));
    accuracy = (true_positives) / (true_positives+false_negatives) * 100

    return accuracy
