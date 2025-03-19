import pandas as pd
import anthropic
import time
from tqdm import tqdm
import os
# Add these imports for topic modeling
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import sys

nltk.data.path.append("C:/Users/AnneL/AppData/Roaming/nltk_data")
nltk.download('stopwords', quiet=False, download_dir="C:/Users/AnneL/AppData/Roaming/nltk_data")
nltk.download('punkt_tab', quiet=False, download_dir="C:/Users/AnneL/AppData/Roaming/nltk_data")

def verify_nltk_resources():
    try:
        stopwords.words('english')
        word_tokenize("Test sentence")
        return True
    except LookupError as e:
        # Error handling...
        return False

# Create a dedicated function to download and verify NLTK resources
def setup_nltk_resources():
    # Define the path where NLTK data should be stored
    nltk_data_dir = "C:/Users/AnneL/AppData/Roaming/nltk_data"
    
    # Create directory if it doesn't exist
    os.makedirs(nltk_data_dir, exist_ok=True)
    
    # Add to NLTK's search path
    nltk.data.path.append(nltk_data_dir)
    
    # Print current search paths for debugging
    print(f"NLTK data search paths: {nltk.data.path}")
    
    # List of required resources
    resources = ['punkt', 'stopwords']
    
    # Download each resource and verify it's accessible
    for resource in resources:
        try:
            # First check if the resource is already available
            nltk.data.find(f'tokenizers/{resource}' if resource == 'punkt' else f'corpora/{resource}')
            print(f"Resource '{resource}' is already available.")
        except LookupError:
            # If not available, download it
            print(f"Downloading NLTK resource: {resource}")
            download_success = nltk.download(resource, download_dir=nltk_data_dir, quiet=False)
            
            if not download_success:
                print(f"Failed to download {resource}. Please check your internet connection.")
                return False
            
            # Verify the download was successful
            try:
                nltk.data.find(f'tokenizers/{resource}' if resource == 'punkt' else f'corpora/{resource}')
                print(f"Successfully downloaded and verified: {resource}")
            except LookupError as e:
                print(f"Download seemed to work but resource still not available: {e}")
                print(f"You may need to manually download {resource}.")
                return False
    
    # Final verification
    try:
        # Test that we can actually use the resources
        stopwords.words('english')
        word_tokenize("Test sentence")
        print("All NLTK resources verified successfully!")
        return True
    except Exception as e:
        print(f"Error verifying NLTK resources: {e}")
        return False

# Replace your current NLTK setup code with this
if not setup_nltk_resources():
    print("Exiting due to missing NLTK resources")
    sys.exit(1)


# Load your data (assuming you have a DataFrame with a text column)
df = pd.read_csv(r"C:\Users\AnneL\Downloads\combined_demo.csv", sep=";")

# Create a new column for summaries
# Create a new column for topics
df['topic'] = -1

# For demonstration purposes, you can work with more data for topic modeling
# df = df.head(10)  # Comment this out to use more data for better topic modeling

# Function to preprocess text
def preprocess_text(text):
    if not isinstance(text, str):
        return ""
    
    # Tokenize and convert to lowercase
    tokens = word_tokenize(text.lower())
    
    # Remove stopwords (you can add Dutch stopwords if needed)
    stop_words = set(stopwords.words('english') + stopwords.words('dutch'))
    tokens = [token for token in tokens if token not in stop_words and len(token) > 2]
    
    return " ".join(tokens)

# Apply preprocessing to the Answer column
df['processed_text'] = df['Answer'].apply(preprocess_text)

# Remove empty answers
df_for_topics = df[df['processed_text'] != ""].copy()

# Create a document-term matrix
vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=1000)
dtm = vectorizer.fit_transform(df_for_topics['processed_text'])

# Number of topics to identify - adjust as needed
num_topics = 5

# Create and fit the LDA model
lda_model = LatentDirichletAllocation(n_components=num_topics, 
                                      random_state=42,
                                      learning_method='online')
lda_output = lda_model.fit_transform(dtm)

# Assign the most likely topic to each document
df_for_topics['topic'] = lda_output.argmax(axis=1)

# Map the topic assignments back to the original dataframe
topic_mapping = dict(zip(df_for_topics.index, df_for_topics['topic']))
df['topic'] = df.index.map(topic_mapping).fillna(-1).astype(int)

# Display the top words for each topic
feature_names = vectorizer.get_feature_names_out()
# Create a DataFrame with topics and their top words
topic_words_data = []
for topic_idx, topic in enumerate(lda_model.components_):
    top_words_idx = topic.argsort()[:-11:-1]  # Get indices of top 10 words
    top_words = [feature_names[i] for i in top_words_idx]
    topic_words_data.append({
        'topic_number': topic_idx,
        'top_words': ', '.join(top_words)
    })
    print(f"Topic {topic_idx}: {', '.join(top_words)}")

topic_words_df = pd.DataFrame(topic_words_data)

# Display topic distribution
topic_counts = df[df['topic'] >= 0]['topic'].value_counts().sort_index()
print("\nTopic distribution:")
print(topic_counts)


import anthropic
api_key = os.environ.get('CLAUDE-API')

# Initialize the Anthropic client with your API key
client = anthropic.Anthropic(
    api_key=api_key,  # Replace with your actual API key
)

def generate_code(prompt):
    return client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    ).content[0].text

topic_words_df['summary'] = ''

# Loop through each row in the DataFrame
for index, row in tqdm(topic_words_df.iterrows(), total=len(topic_words_df), desc="Generating summaries"):
    # Check if the answer has at least 7 words
    if row['top_words'] and isinstance(row['top_words'], str) and len(row['top_words'].split()) >= 7:
        try:
            # Generate a summary for answers with 7+ words
            summary = generate_code(f"Ik heb de volgende woorden uit een topic model gekregen, ik wil deze topics omzetten naar een onderwerp in maximaal twee woorden:\n\n{row['top_words']}. Ik wil graag alleen het onderwerp terug krijgen als antwoord. Dus geen uitleg og zinnen. 'Niet van toepassing' is geen goed topic, zoek hier een alternatief voor")
            # Store the summary in the DataFrame
            topic_words_df.at[index, 'summary'] = summary
            # Add a small delay to avoid rate limiting
            time.sleep(0.5)
        except Exception as e:
            print(f"Error processing row {index}: {e}")
    else:
        # For answers with fewer than 7 words, leave the summary empty
        topic_words_df.at[index, 'summary'] = ''

topic_words_df.rename(columns={'topic_number': 'topic'}, inplace=True)
df_final = pd.merge(df, topic_words_df, 'left')

# Save the results to a new CSV file (optional)
df.to_csv('summarized_data.csv', index=False)

df.drop(columns=['summary'], inplace=True)
