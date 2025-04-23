import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from transformers import pipeline

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

stemmer = PorterStemmer()

def clean_review(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r'@[^\s]+', '', text)  # eliminar menciones
    text = re.sub(r'https?://\S+', '', text)  # eliminar URLs
    text = re.sub(r'#', '', text)  # eliminar signos de #
    text = text.lower()  # pasar a minúsculas
    text = re.sub(r'\s+', ' ', text)  # remover espacios duplicados
    text = re.sub(r'[^\w\s]', '', text)  # remover puntuación
    text = re.sub(r'\d+', '', text)  # remover números
    tokens = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered = [word for word in tokens if word not in stop_words]
    stemmed = [stemmer.stem(word) for word in filtered]
    
    return ' '.join(stemmed)

classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)
def classify_emotion(review):
    truncated_review = review[:720]
    return classifier(truncated_review)[0][0]