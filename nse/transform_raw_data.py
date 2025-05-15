
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


input_path = r'C:\Users\anne.leemans\Stichting Hogeschool Utrecht\FCA-DA-P - Analytics\Open antwoorden\NSE'
year = 2024
input_file_name = f'nse{year}.csv'


def transform_nse_data(input_path, input_file_name, year):
    
    """
    Transforms the NSE open answers data structure from wide to long format.

    Parameters:
    input_path (str): The directory path where the input CSV file is located.
    input_file_name (str): The name of the input CSV file.

    Returns:
    None
    """
    # Construct the full path to the input file
    full_path = os.path.join(input_path, input_file_name)

    # Read the CSV file
    df = pd.read_csv(full_path, sep=';', encoding='utf-8-sig')

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
    transformed_df = pd.DataFrame(transformed_data, columns=['Id', 'Answer', 'Q Name'])
    
    # Add a Q dimension table
    q_name_df = transformed_df[['Q Name']].drop_duplicates()
    q_name_df.reset_index(inplace=True)
    q_name_df.columns = ['Q ID', 'Q Name']
    
    # Add ID to transformed data
    transformed_df = transformed_df.merge(q_name_df, 'left', left_on='Q Name', right_on='Q Name')
    transformed_df.drop(columns=['Q Name'], inplace=True)
    
    # Save the transformed DataFrame to a new Excel file
    output_file_path = os.path.join(input_path, f"nse_transformed_{year}.csv")
    transformed_df.to_csv(output_file_path, index=False, sep=';')
    
    # Save DIM data to file
    output_file_path = os.path.join(input_path, f"nse_q_dim_{year}.csv")
    q_name_df.to_csv(output_file_path, index=False, sep=';')
    
    # Print a success message
    print("The data has been successfully transformed and saved to nse_transformed.csv")

transform_nse_data(input_path, input_file_name, year)