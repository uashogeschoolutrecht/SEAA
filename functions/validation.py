## Input is DF with at least the following columns:
# 1. AVG: classification of SEAA algorithm on whether row has AVG data = 1 or 0, 
# 2. actual__AVG = 1 or 0 (whether column actually has AVG data)
# efficiency --> number of detected cases without AVG / total cases
# accuracy   --> number of correctly detected cases / total cases

def SEAA_efficiency(df):
    '''df = dataframe with column ['AVG'] that contains classification of SEAA algorithm whether row has AVG data (1) or not (0). '''

    # Calculate efficiency (%)
    efficiency = (1 - (sum(df['AVG']) / len(df)))*100

    return efficiency

    ## Calculate accuracy
    # Load validation data for accuracy test
    logedin_user = os.getlogin()
    path = f"C:\\Users\\{logedin_user}\\Stichting Hogeschool Utrecht\\FCA-DA-P - Analytics\\Open antwoorden\\"
    acctestdata_df = pd.read_csv(f'{path}{"fake data nse open vragen.csv"}', sep =';')

    # Clean validation data
    acctestdata_df['antwoord_clean'] = acctestdata_df['antwoord'].str.lower() 
    acctestdata_df = acctestdata_df[~acctestdata_df['antwoord_clean'].isnull()]
    acctestdata_df.reset_index(inplace=True,drop=True)

    #Run SEAA on accuracy testdata 
    # Below code is currently code + paste from loaddata.py. Should be replaced with SEAA function
    acctestdata_df['AVG'] = 0
    N = len(acctestdata_df)
    for i in range(0,N):
        test = acctestdata_df['antwoord_clean'][i]
        test_df = pd.DataFrame({'WoordenClean':re.findall(r'(\w+)', test)})
        check_df = pd.merge(test_df,words,'left')
        check_df['AVG'] = np.where(check_df['AVG'].isnull(),1,0)

        if check_df['AVG'].sum() >= 1:
            acctestdata_df.loc[i,'AVG'] = 1
        else:
            acctestdata_df.loc[i,'AVG'] = 0
        print(f'{round(i/N*100,0)}%')

    print('done')

    # Calculate accuracy
    # When seaa_avg is 1, it means that SEAA  determined the string to be containing AVG data. 
    # This is true when the actual string did contain any privacy-related 
    # fields (AVG = 1).
    # When seaa_avg is 0, SEAA determined that the string is AVG-free, so it will not
    # contain AVG data (AVG = 0).
    #
    # When assessing the algorithm SEAA the output of SEAA for a case falls 
    # into one of the following four categories:
    # True positive: seaa_avg = 1 and AVG = 1
    # True negative: seaa_avg = 0 and AVG = 0
    # False positive: seaa_avg = 1 and AVG = 0
    # False negative = seaa_avg = 0 and AVG = 1
    #
    # Accuracy = (true positives + true negatieve) / total cases
    true_positives = sum((acctestdata_df['AVG validatie']==1) & (acctestdata_df['AVG'] == 1));
    true_negatives = sum((acctestdata_df['AVG validatie']==0) & (acctestdata_df['AVG'] == 0));
    accuracy = (true_positives + true_negatives) / len(acctestdata_df) * 100
