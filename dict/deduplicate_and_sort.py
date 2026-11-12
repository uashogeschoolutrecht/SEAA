"""Deduplicate and sort a dictionary file, removing surrounding whitespace.

Example (from the dict directory): python deduplicate_and_sort.py whitelist.txt
"""

import argparse


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('dict_file', help='dictionary filename to process')
    file_path = parser.parse_args().dict_file

    # Read the file and process the lines
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Count lines with leading or trailing whitespace; the cleanup below removes it.
    whitespace_line_count = sum(
        1 for line in lines
        if line.rstrip('\r\n') != line.rstrip() or line.lstrip() != line
    )
    if whitespace_line_count:
        print(f"Removed leading or trailing whitespace from {whitespace_line_count} line(s).")

    # Keep the header
    header = lines[0].strip() if lines else ''

    # Process the rest: remove duplicates and strip whitespace
    unique_lines = set(line.strip() for line in lines[1:] if line.strip())

    # Sort the lines alphabetically (case-insensitive)
    sorted_lines = sorted(unique_lines, key=lambda line: line.lower())

    # Write the header and sorted lines back to the same file
    with open(file_path, 'w', encoding='utf-8') as file:
        if header:
            file.write(header + '\n')
        for line in sorted_lines:
            file.write(line + '\n')


if __name__ == '__main__':
    main()
