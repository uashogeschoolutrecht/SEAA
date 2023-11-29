## Input is DF with at least the following columns:
# 1. 'seaa_avg': determined whether column has AVG data = 1 or 0, 
# 2. AVG = 1 or 0 (whether column actually has AVG data)
# efficiency --> number of detected cases without AVG / total cases
# accuracy   --> number of correctly detected cases / total cases

import numpy as np  #Needed for random number generator
import pandas as pd

# Load data
logedin_user = os.getlogin()
path = f"C:\\Users\\{logedin_user}\\Stichting Hogeschool Utrecht\\FCA-DA-P - Analytics\\Open antwoorden\\"
file_name = "nse2023openant.csv"
nseant_df = pd.read_csv(f'{path}{file_name}', sep =';')

# Add fake data column 'seaa_avg' (with random value 0 or 1) 
# --> replace with run of SEAA when ready
nseant_df['seaa_avg'] = np.random.randint(0,2, nseant_df.shape[0])

# Calculate efficiency
efficiency = sum(nseant_df['seaa_avg']) / len(nseant_df)

## Calculate accuracy
# Load accuracy testdata
acctestdata_df = pd.read_csv(f'{path}{"fake data nse open vragen.csv"}', sep =';')

#Run SEAA on accuracy testdata 
# Add fake data column 'seaa_avg' (with random value 0 or 1) 
# --> replace with run of SEAA when ready
acctestdata_df['seaa_avg'] = np.random.randint(0,2, acctestdata_df.shape[0])

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
