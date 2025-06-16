# Mini script to deduplicate and sort a dict file

# Define the file path
file_path = 'whitelist.txt'  # Replace with your actual file name

# Read the file and process the lines
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

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
