import pandas as pd
import re
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np

# Read the CSV file with semicolon delimiter
df = pd.read_csv('files/POE_fake_reviews.csv', delimiter=';')

def check_privacy_data(text):
    patterns = [
        r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',  # Full names
        r'\b[A-Z][a-z]+ [A-Z]\.',         # Names with initial
        r'\b[A-Z][a-z]+ [A-Z][a-z]+',     # First name + Last name
        r'Dr\. [A-Z][a-z]+',              # Doctor titles
        r'Professor [A-Z][a-z]+'          # Professor titles
    ]
    
    for pattern in patterns:
        if re.search(pattern, text):
            return 1
    return 0

# Privacy check
df['Contains_Privacy_Data'] = df['Review'].apply(check_privacy_data)

# Sentiment analysis
def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

df['Sentiment'] = df['Review'].apply(get_sentiment)

# Topic modeling
# Prepare the text data
vectorizer = TfidfVectorizer(
    max_features=1000,
    stop_words='english',
    max_df=0.95,
    min_df=2
)
tfidf = vectorizer.fit_transform(df['Review'])

# Create and fit LDA model
n_topics = 5  # You can adjust this number
lda = LatentDirichletAllocation(
    n_components=n_topics,
    random_state=42,
    max_iter=10
)
lda_output = lda.fit_transform(tfidf)

# Get dominant topic for each document
topic_names = [f"Topic {i+1}" for i in range(n_topics)]
df['Dominant_Topic'] = [topic_names[i] for i in np.argmax(lda_output, axis=1)]

# Print top words for each topic (optional)
feature_names = vectorizer.get_feature_names_out()
for topic_idx, topic in enumerate(lda.components_):
    top_words = [feature_names[i] for i in topic.argsort()[:-10 - 1:-1]]
    print(f"Topic {topic_idx + 1}: {', '.join(top_words)}")

# Save the updated CSV
df.to_csv('files/POE_fake_reviews_with_analysis.csv', sep=';', index=False)




df[['Review']]