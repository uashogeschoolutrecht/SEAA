## Input is DF with at least the following columns:
# 1. AVG: classification of SEAA algorithm on whether row has AVG data = 1 or 0, 
# 2. actual__AVG = 1 or 0 (whether column actually has AVG data)
# efficiency --> number of detected cases without AVG / total cases
# accuracy   --> number of correctly detected cases / total cases

import numpy as np  #Needed for random number generator
import pandas as pd
import os

# Get data that was run through SEAA
nseant_df = df;

# Calculate efficiency (%)
efficiency = (1 - (sum(nseant_df['AVG']) / len(nseant_df)))*100

## Calculate accuracy
# Load accuracy testdata
logedin_user = os.getlogin()
path = f"C:\\Users\\{logedin_user}\\Stichting Hogeschool Utrecht\\FCA-DA-P - Analytics\\Open antwoorden\\"
acctestdata_df = pd.read_csv(f'{path}{"fake data nse open vragen.csv"}', sep =';')

#Run SEAA on accuracy testdata 
# Add fake data column 'seaa_avg' (with random value 0 or 1) 
# --> replace with run of SEAA when ready
acctestdata_df['AVG'] = np.random.randint(0,2, acctestdata_df.shape[0])

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
true_positives = sum((acctestdata_df['AVG?']==1) & (acctestdata_df['seaa_avg'] == 1));
true_negatives = sum((acctestdata_df['AVG?']==0) & (acctestdata_df['seaa_avg'] == 0));
accuracy = (true_positives + true_negatives) / len(acctestdata_df)
