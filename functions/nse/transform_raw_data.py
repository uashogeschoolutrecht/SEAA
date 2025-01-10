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

def transform_nse_data(input_path, input_file_name):
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
    df = pd.read_csv(full_path, sep=';')

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
    transformed_df = pd.DataFrame(transformed_data, columns=['Id', 'Answer', 'Q Number'])

    # Save the transformed DataFrame to a new Excel file
    output_file_path = os.path.join(input_path, "nse_transformed.xlsx")
    transformed_df.to_excel(output_file_path, index=False)

    # Print a success message
    print("The data has been successfully transformed and saved to nse_transformed.xlsx")

# Example usage:
# transform_nse_data("C:\\Users\\YourUsername\\Path\\To\\Data\\", "nse2023.csv")