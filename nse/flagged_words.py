import pandas as pd
import os

# Define the paths
base_path = r"C:\Users\anne.leemans\Stichting Hogeschool Utrecht\FCA-DA-P - Analytics\Open antwoorden\output"
input_files = {
    "2024": os.path.join(base_path, "SEAA_nse2024_output.csv"),
    "2025": os.path.join(base_path, "SEAA_nse2025_output.csv")
}
output_files = {
    "2024": os.path.join(base_path, "unknown_words_2024.csv"),
    "2025": os.path.join(base_path, "unknown_words_2025.csv")
}

def process_file(input_file, output_file):
    try:
        # Read the CSV file
        df = pd.read_csv(input_file)
        
        # Filter for Dutch (nl) or Afrikaans (af) language
        df_filtered = df[df['language'].isin(['nl', 'af'])]
        
        # Extract words from unknown_words column
        all_words = []
        for word_list in df_filtered['unknown_words'].dropna():
            # Split by comma and strip whitespace
            words = [word.strip() for word in word_list.split(',')]
            all_words.extend(words)
        
        # Remove duplicates and empty strings
        unique_words = list(set([word for word in all_words if word]))
        
        # Create a DataFrame with one word per row
        result_df = pd.DataFrame({'word': unique_words})
        
        # Save to CSV
        result_df.to_csv(output_file, index=False)
        
        print(f"Successfully processed {input_file}")
        print(f"Found {len(unique_words)} unique unknown words")
        print(f"Output saved to {output_file}")
        
    except Exception as e:
        print(f"Error processing {input_file}: {str(e)}")

# Process both files
for year, input_file in input_files.items():
    process_file(input_file, output_files[year])

print("Processing complete!")
