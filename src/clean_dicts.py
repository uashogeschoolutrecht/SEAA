import os

# Get the path to the sibling 'dict' folder
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
dict_dir = os.path.join(parent_dir, 'dict')

# Read the wordlist.txt file and convert all words to lowercase for comparison
wordlist_path = os.path.join(dict_dir, 'wordlist.txt')
with open(wordlist_path, 'r', encoding='utf-8') as wordlist_file:
    wordlist = set(word.strip().lower() for word in wordlist_file)

# Read the plaatsnamen.txt file
plaatsnamen_path = os.path.join(dict_dir, 'plaatsnamen.txt')
with open(plaatsnamen_path, 'r', encoding='utf-8') as plaatsnamen_file:
    plaatsnamen = [line.strip() for line in plaatsnamen_file]

# Filter out words that appear in the wordlist (case-insensitive comparison)
filtered_plaatsnamen = [plaats for plaats in plaatsnamen if plaats.lower() not in wordlist]

# Write the filtered list back to plaatsnamen.txt, preserving original capitalization
with open(plaatsnamen_path, 'w', encoding='utf-8') as output_file:
    for plaats in filtered_plaatsnamen:
        output_file.write(plaats + '\n')

print(f"Removed {len(plaatsnamen) - len(filtered_plaatsnamen)} words from plaatsnamen.txt")
