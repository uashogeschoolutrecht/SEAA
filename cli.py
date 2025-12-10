#!/usr/bin/env python3
"""
Command-line interface for the SEAA (Semi-automatic Anonymization Algorithm) tool.
This tool processes and anonymizes open-ended survey responses.

Usage:
    python cli.py <input_folder> <output_folder> [options]
    
Examples:
    python cli.py ./data ./output
    python cli.py ./data ./output --file specific_file.csv
    python cli.py ./data ./output --limit 1000
"""

import argparse
import os
import sys
from main import process_answers


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="SEAA - Semi-automatic Anonymization Algorithm for survey responses",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s ./data ./output                      Process all CSV files in ./data
  %(prog)s ./data ./output --file input.csv     Process specific file only
  %(prog)s ./data ./output --limit 1000         Process first 1000 rows only

Input CSV Requirements:
  - Semicolon-separated (;)
  - Columns: Answer, respondent_id, question_id
        """
    )
    
    parser.add_argument('input_folder', help='Folder containing input CSV file(s)')
    parser.add_argument('output_folder', help='Folder where output files will be saved')
    parser.add_argument('-f', '--file', help='Specific CSV file to process (optional)')
    parser.add_argument('-l', '--limit', type=int, default=-1,
                       help='Limit number of rows to process (-1 for all)')
    
    args = parser.parse_args()
    
    # Validate input folder exists
    if not os.path.exists(args.input_folder):
        print(f"Error: Input folder '{args.input_folder}' not found.")
        sys.exit(1)
    
    # Validate specific file if provided
    if args.file:
        file_path = os.path.join(args.input_folder, args.file)
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found.")
            sys.exit(1)
    
    try:
        process_answers(
            input_folder=args.input_folder,
            output_folder=args.output_folder,
            input_file=args.file,
            limit=args.limit
        )
        print("\nProcessing complete!")
        sys.exit(0)
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()