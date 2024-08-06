# Install required libraries
!pip install requests
!pip install bs4
!pip install nltk

# Program:
import requests
from bs4 import BeautifulSoup # Used to parse webpages
import re # Used for Regular Expressions
import nltk # Used for Language Analysis
from nltk.corpus import stopwords

# Download required data from Natural Language ToolKit
nltk.download('punkt')
nltk.download('stopwords')

def fetch_description(topic):
    topic = topic.replace(' ', '_') # URL cannot contain spaces, replace with Underscores
    try:
        # Use Wikipedia to fetch data
        r = requests.get(f'https://en.wikipedia.org/api/rest_v1/page/html/{topic}')
        r.raise_for_status()
        soup = BeautifulSoup(r.content, 'html.parser')
        html_paragraphs = soup.find_all('p')
        for p in html_paragraphs:
            # Remove the Wikipedia Citations (numbers within brackets)
            cleaned_text = re.sub(r'\[[0-9]+\]', '', p.text).strip()
            if cleaned_text:
                return cleaned_text
    except Exception as e:
        return f"Unexpected error occurred for {topic}: {e}"
    return "No information available for this topic."

def chatbot():
    def preprocess_text(text):
        # Replace non word characters like ' , ! with spaces
        # \W matches with non word characters, + matches multiples non word characters
        text = re.sub(r'\W+', ' ', text)
        # Tokenization breaks text into individual tokens- words and punctuations
        words = nltk.word_tokenize(text)
        # Stop words are common words like how, what, the, and, etc.
        stop_words = set(stopwords.words('english'))
        # Remove these words to filter out keywords
        filtered_words = [word for word in words if word not in stop_words]
        return filtered_words

    print("Welcome to the Chatbot! Type 'exit' to quit.")
    while True:
        query = input("You: ")
        if query.lower() == 'exit':
            break
        query_words = preprocess_text(query)
        if not query_words:
            print("Bot: Please enter a valid query.\n")
            continue
        topic = ' '.join(query_words[:])
        response = fetch_description(topic)
        print(f"Bot: {response}\n")

if __name__ == "__main__":
    chatbot()
