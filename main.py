# run the main functions
import pandas as pd
import os 

# import NSE open answers
logedin_user = os.getlogin()
path = f"C:\\Users\\{logedin_user}\\Stichting Hogeschool Utrecht\\FCA-DA-P - Analytics\\Open antwoorden\\"
file_name = "nse2023openant.csv"
nseant_df = pd.read_csv(f'{path}{file_name}', sep =';')

# import Dutch word list
file_name = "Opentaal_woordenlijst.txt"
word_list_df = pd.read_csv(f"{path}{file_name}", sep =';')