# Kind of hard-coded file to transform the NSE open answers data structure
# Input is:
# Id    Question 1    Question 2    etc. 
# 1     answerA       answerC
# 2     answerAA
# 3                   answerB
#
# Output is:
# Id    Answer      Question
# 1     answerA     Question 1
# 1     answerC     Question 2
# 2     answerAA    Question 1
# 3     answerB     Question 2
#
# Hard-coded sections are: 
# - input filename
# - column numbers that contain the questions
# - output filename


import os 
import pandas as pd

## Import NSE open answers
logedin_user = os.getlogin()
path = f"C:\\Users\\{logedin_user}\\Stichting Hogeschool Utrecht\\FCA-DA-P - Analytics\\Open antwoorden\\"
file_name = "nse2023.csv"

path = f"{path}data\\"
df = pd.read_csv(f'{path}{file_name}', sep =';')

# Initialize an empty list to store the transformed data
transformed_data = []
# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    # Get the ID
    idea_id = row['Id']
    # Iterate over each question column
    for col in df.columns[[12, 13, 15, 17, 19, 21, 23, 25]]:
        # Get the answer and question number
        answer = row[col] 
        q_number = col
        # Append the transformed data to the list if the answer is not empty
        if pd.notna(answer): 
            transformed_data.append([idea_id, answer, q_number])
            
# Create a new DataFrame with the transformed data
transformed_df = pd.DataFrame(transformed_data, columns=['Id','Answer','Q Number'])
# Save the transformed DataFrame to a new Excel file
output_file_path = f"{path}nse2023_transformed.xlsx"
transformed_df.to_excel(output_file_path, index=False)
# Print a success message
print("The data has been successfully transformed and saved to transformed_data.xlsx")