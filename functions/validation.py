## Input is DF with at least the following columns:
# 1. Succesfully anonimised column = 1 or 0, 
# 2. AVG = 1 or 0 (whether )
# efficiency --> number of anonimised cases / total cases
# accuracy   --> number of correctly detected cases / total cases

import numpy as np  #Needed for random number generator

# Load data
logedin_user = os.getlogin()
path = f"C:\\Users\\{logedin_user}\\Stichting Hogeschool Utrecht\\FCA-DA-P - Analytics\\Open antwoorden\\"
file_name = "nse2023openant.csv"
nseant_df = pd.read_csv(f'{path}{file_name}', sep =';')

# Create fake data column 'Success' 
nseant_df['Success'] = np.random.randint(0,2, nseant_df.shape[0])

# Calculate efficiency
efficiency = sum(nseant_df['Success']) / len(nseant_df)