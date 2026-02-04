"""
SEAA: Semi-automatic Anonymization Algorithm

Process and anonymize open-ended survey responses.

Required Input Format:
The input CSV file must be semicolon-separated (;) and contain the following columns:
- Answer: The actual text responses
- respondent_id: Unique identifier for each respondent
- question_id: Identifier for the question being answered

Output:
- SEAA_output_{date}.csv: Main analysis results with anonymized answers
- avg_words_count_{date}.csv: List of unknown words for review
"""

import os
import pandas as pd
from datetime import datetime
from typing import Optional
from src.load_seaa_data import load_data, load_dictionary
from src.SEAA import SEAA
from src.AVG_list import AVG_list

def process_answers(input_folder: str, output_folder: str, input_file: Optional[str] = None, limit: int = -1, answer_column: str = 'Answer') -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Process open-ended survey responses and anonymize privacy-sensitive information.
    
    Args:
        input_folder: Path to folder containing input CSV file(s)
        output_folder: Path to folder where output files will be saved
        input_file: Optional specific filename. If None, processes all CSV files in input_folder
        limit: Limit the number of responses to process (-1 for all)
    
    Returns:
        Tuple of (results_df, avg_words_df)
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Determine which files to process
    if input_file:
        files_to_process = [input_file]
    else:
        files_to_process = [f for f in os.listdir(input_folder) if f.endswith('.csv')]
    
    if not files_to_process:
        raise ValueError(f"No CSV files found in {input_folder}")
    
    # Load dictionaries
    dictionary_df = _load_known_words()
    flag_df = _load_flag_words()
    
    all_results = []
    all_avg_words = []
    
    for file in files_to_process:
        print(f"\nProcessing: {file}")
        
        # Load and prepare data
        df = load_data(input_folder, file, answer_column)
        
        # Apply limit if specified
        if limit > 0:
            df = df.head(limit)
        
        # Run SEAA algorithm
        result_df = SEAA(df, dictionary_df, flag_df)
        
        # Get unknown words that are not yet flagged (only for Dutch text)
        dutch_results = result_df[result_df["language"] == 'nl'].copy()
        avg_words_df = AVG_list(dutch_results, flag_df)
        
        # Filter out words already in flag list
        avg_words_df = avg_words_df.merge(flag_df, 'left', left_on='AVG_woord', right_on='words')
        avg_words_df = avg_words_df[avg_words_df['words'].isna()].drop(columns=['words', 'dict_type', 'is_known'], errors='ignore')
        
        all_results.append(result_df)
        all_avg_words.append(avg_words_df)
    
    # Combine all results
    final_results = pd.concat(all_results, ignore_index=True) if all_results else pd.DataFrame()
    final_avg_words = pd.concat(all_avg_words, ignore_index=True) if all_avg_words else pd.DataFrame()
    
    # Aggregate word counts if processing multiple files
    if len(all_avg_words) > 1 and not final_avg_words.empty:
        final_avg_words = final_avg_words.groupby('AVG_woord')['Count'].sum().reset_index()
        final_avg_words = final_avg_words.sort_values('Count', ascending=False)
    
    # Save results
    datum = datetime.today().strftime("%Y%m%d")
    
    results_path = os.path.join(output_folder, f"SEAA_output_{datum}.csv")
    final_results.to_csv(results_path, sep=';', encoding='utf-8-sig', index=False)
    print(f"\nResults saved to: {results_path}")
    
    avg_words_path = os.path.join(output_folder, f"avg_words_count_{datum}.csv")
    final_avg_words.to_csv(avg_words_path, sep=';', encoding='utf-8-sig', index=False)
    print(f"Unknown words saved to: {avg_words_path}")
    
    # Print summary
    privacy_count = len(final_results[final_results['contains_privacy'] == 1])
    print(f"\nSummary:")
    print(f"  Total responses processed: {len(final_results)}")
    print(f"  Responses with privacy concerns: {privacy_count}")
    print(f"  Unknown words to review: {len(final_avg_words)}")
    
    return final_results, final_avg_words

def _load_known_words() -> pd.DataFrame:
    """Load dictionary of known safe words."""
    word_list_df = load_dictionary(file_name="wordlist.txt", dict_type='known')
    whitelist_df = load_dictionary(file_name='whitelist.txt', dict_type='known')
    return pd.concat([word_list_df, whitelist_df], ignore_index=True)

def _load_flag_words() -> pd.DataFrame:
    """Load dictionary of words that should be flagged."""
    flag_files = [
        ('illness.txt', 'illness'), 
        ('studiebeperking.txt', 'disability'), 
        ('names.txt', 'name'), 
        ('blacklist.txt', 'blacklist'), 
        ('plaatsnamen.txt', 'plaatsnaam'),
        ('familie.txt', 'familie'),
        ('persoonlijke_omstandigheden.txt', 'persoonlijke_omstandigheden')
    ]
    
    flag_df = pd.DataFrame()
    for file_name, file_type in flag_files:
        temp_df = load_dictionary(file_name=file_name, dict_type=file_type)
        flag_df = pd.concat([flag_df, temp_df], ignore_index=True)
    
    return flag_df

if __name__ == "__main__":
    # Example usage - modify these paths as needed
    INPUT_FILE = r'Open Antwoorden 100D 2025-2026.csv'
    INPUT_FOLDER = r"C:\Users\AnneL\Stichting Hogeschool Utrecht\FCA-DA-P - Inleesbestanden\Domein Education Analytics\SEAA\100 dagen monitor\input"
    OUTPUT_FOLDER = r"C:\Users\AnneL\Stichting Hogeschool Utrecht\FCA-DA-P - Inleesbestanden\Domein Education Analytics\SEAA\100 dagen monitor\output"
    ANSWER_COLUMN = 'Antwoord'

    process_answers(
        input_file=INPUT_FILE,
        input_folder=INPUT_FOLDER,
        output_folder=OUTPUT_FOLDER,
        answer_column=ANSWER_COLUMN
    )