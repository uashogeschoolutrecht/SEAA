import os 
import pandas as pd
from functions.loadSEAAdata import loaddata
from functions.loadSEAAdata import loaddict

# import NSE open answers
logedin_user = os.getlogin()
if logedin_user == 'pim.lamberts': #User Pim does not see the parent folder
    path = f"C:\\Users\\{logedin_user}\\Stichting Hogeschool Utrecht\\FCA-DA-P - Open antwoorden\\"
else:
    path = f"C:\\Users\\{logedin_user}\\Stichting Hogeschool Utrecht\\FCA-DA-P - Analytics\\Open antwoorden\\"
file_name = "nse2023openant.csv"
nseant_df = loaddata(path, file_name)

# import dictionaries
# Dutch word dictionary
word_list_df = loaddict(path=path, file_name="wordlist.txt")

# white list (words not part of the Dutch dictionary but considered safe regardless)
whitelist_df = loaddict(path=path, file_name='whitelist.txt')
word_list_df = pd.concat([word_list_df, whitelist_df], ignore_index=True)

# illnesses dictionaries
illness_df = loaddict(path=path, file_name='illness.txt', type='illness')

# blacklist dictionary
blacklist_df = loaddict(path=path, file_name='blacklist.txt')

# merge all words that should be flagged
flag_df = pd.concat([illness_df, blacklist_df], ignore_index=True)

# Run SEAA
from functions.SEAA import SEAA
result_df = SEAA(nseant_df, word_list_df,flag_df, 50) # <== 4m .7s

# Add Dutch or not Dutch column classificatiion
# If the anwser contains 8 or more words and more than 40 percent of those words are unkown
# the awnser will be classified as not Dutch
import numpy as np
result_df.loc[:,"NL/NietNL"] = "NL"
result_df.loc[:,"NL/NietNL"] = np.where(
    (result_df['total_word_count']>=8) & 
    (result_df['sensitive_word_count'] / result_df['total_word_count']> 0.4),
     "Niet NL",
     "NL")           

# Delete columns after language check   
result_df.drop(columns=['total_word_count','sensitive_word_count'], inplace=True)

from functions.validation import SEAA_efficiency
# Calculate efficiency of SEAA
efficiency = SEAA_efficiency(result_df[result_df["NL/NietNL"]=='NL'])

# Calculate accuracy of SEAA
validation_df = loaddata(path, "nse annoteringen.csv")

from functions.validation import SEAA_accuracy
accuracy = SEAA_accuracy(validation_df, word_list_df, illness_df)

# Extract AVG words with count
from AVG_list import AVG_list
avg_words_df = AVG_list(result_df[result_df["NL/NietNL"]=='NL'])

# Check if word is in the flagged list
avg_words_df= avg_words_df.merge(flag_df,'left', left_on='AVG_woord',right_on='words')

# remove rows with blacklisted words and remove redundant columns
avg_words_df = avg_words_df[avg_words_df['words'].isna()].drop(columns='words')

from functions.expand_dicts import expand_dicts
whitelist_df, blacklist_df = expand_dicts(avg_words_df, whitelist_df, blacklist_df)

whitelist_df.to_csv(f'{path}//dict//whitelist.txt',index=False)
blacklist_df.to_csv(f'{path}//dict//blacklist.txt',index=False)

# Save word count list to file,
file_name = 'avg_words_count.csv'
avg_words_df.to_csv(f'{path}{file_name}', sep =';')