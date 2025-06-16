#!/usr/bin/env python3
"""
Command-line interface for the SEAA (Semi-Automated Analysis) tool.
This tool processes and analyzes open-ended survey responses.
"""

import argparse
import os
import sys
import pandas as pd
from main import main
from src.expand_dicts import process_word_decision


def process_csv(input_file, output_file=None, limit=-1):
    """
    Process a CSV file with the SEAA tool.
    
    Args:
        input_file (str): Path to the input CSV file
        output_file (str): Path for the output CSV file (optional)
        limit (int): Limit the number of responses to process (-1 for all)
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return False
        
    if not input_file.lower().endswith('.csv'):
        print("Error: Input file must be a CSV file.")
        return False
    
    # Extract directory and filename
    input_dir = os.path.dirname(input_file) or '.'
    filename = os.path.basename(input_file)
    
    # Set default output filename if not provided
    if output_file is None:
        base_name = os.path.splitext(filename)[0]
        output_file = f"{base_name}_SEAA_output.csv"
    
    print(f"Processing file: {input_file}")
    print(f"Output will be saved to: {output_file}")
    
    try:
        # Create necessary directories
        os.makedirs('data', exist_ok=True)
        os.makedirs('output', exist_ok=True)
        
        # Progress callback for CLI
        def progress_callback(percentage, phase):
            print(f"{phase.capitalize()}: {percentage}%", end='\r')
            if percentage == 100:
                print(f"{phase.capitalize()}: Complete")
        
        # Run the main processing function
        results = main(
            path=input_dir + '/',
            input_file=filename,
            progress_callback=progress_callback,
            limit=limit
        )
        
        results_df = results[0]
        avg_words_df = results[1]
        
        # Save avg_words for potential dictionary expansion
        avg_words_df.to_csv('data/avg_words.csv', index=False)
        
        # Save the main results
        results_df.to_csv(output_file, index=False)
        
        print(f"\nProcessing complete!")
        print(f"Results saved to: {output_file}")
        print(f"Found {len(results_df[results_df['contains_privacy'] == 1])} responses with privacy concerns")
        print(f"Unknown words saved to: data/avg_words.csv ({len(avg_words_df)} words)")
        
        return True
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        return False


def expand_dictionaries():
    """
    Interactive dictionary expansion process.
    """
    try:
        # Check if avg_words.csv exists
        if not os.path.exists('data/avg_words.csv'):
            print("No avg_words.csv file found. Run processing first.")
            return
            
        avg_words_df = pd.read_csv('data/avg_words.csv')
        
        if len(avg_words_df) == 0:
            print("No unknown words to process.")
            return
            
        print(f"Found {len(avg_words_df)} unknown words to review.")
        print("For each word, choose: (w)hitelist, (b)lacklist, or (s)kip")
        print("Press Ctrl+C to quit at any time.\n")
        
        # Load current dictionaries
        whitelist_df = pd.read_csv('dict/whitelist.txt')
        blacklist_df = pd.read_csv('dict/blacklist.txt')
        
        for index, row in avg_words_df.iterrows():
            word = row['AVG_woord']
            count = row['Count']
            
            print(f"Word: '{word}' (appears {count} times)")
            
            while True:
                decision = input("Add to (w)hitelist, (b)lacklist, or (s)kip? ").lower().strip()
                if decision in ['w', 'whitelist']:
                    decision = 'whitelist'
                    break
                elif decision in ['b', 'blacklist']:
                    decision = 'blacklist'
                    break
                elif decision in ['s', 'skip']:
                    print("Skipped.\n")
                    continue
                else:
                    print("Please enter 'w', 'b', or 's'")
            
            if decision != 'skip':
                # Process the decision
                whitelist_df, blacklist_df = process_word_decision(
                    word, decision, whitelist_df, blacklist_df
                )
                
                # Save updated dictionaries
                whitelist_df.to_csv('dict/whitelist.txt', index=False)
                blacklist_df.to_csv('dict/blacklist.txt', index=False)
                
                # Remove the processed word from avg_words.csv
                avg_words_df = avg_words_df[avg_words_df['AVG_woord'] != word]
                avg_words_df.to_csv('data/avg_words.csv', index=False)
                
                print(f"Added '{word}' to {decision}.\n")
        
        print("Dictionary expansion complete!")
        
    except KeyboardInterrupt:
        print("\n\nDictionary expansion interrupted by user.")
    except Exception as e:
        print(f"Error during dictionary expansion: {str(e)}")


def main_cli():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="SEAA - Semi-Automated Analysis tool for survey responses",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s process input.csv                    # Process input.csv
  %(prog)s process input.csv -o results.csv     # Process with custom output name
  %(prog)s process input.csv --limit 1000       # Process only first 1000 rows
  %(prog)s expand                               # Expand dictionaries interactively
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Process command
    process_parser = subparsers.add_parser('process', help='Process a CSV file')
    process_parser.add_argument('input_file', help='Input CSV file path')
    process_parser.add_argument('-o', '--output', help='Output CSV file path')
    process_parser.add_argument('--limit', type=int, default=-1, 
                               help='Limit number of rows to process (-1 for all)')
    
    # Expand command
    expand_parser = subparsers.add_parser('expand', help='Expand dictionaries interactively')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
        
    if args.command == 'process':
        success = process_csv(args.input_file, args.output, args.limit)
        sys.exit(0 if success else 1)
    elif args.command == 'expand':
        expand_dictionaries()


if __name__ == '__main__':
    main_cli() 