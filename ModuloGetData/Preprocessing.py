import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from transformers import pipeline

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt')

stop_words = set(stopwords.words('english'))


def clean_review(text):
    if not isinstance(text, str):
        return ""
    # Conservar signos de exclamación/interrogación (importantes para sentimiento)
    text = re.sub(r'([!?])', r' \1 ', text)  # Añade espacios alrededor
    # Eliminar URLs pero conservar números y algunas puntuaciones
    text = re.sub(r'http\S+|@\S+|#', '', text)
    # Minúsculas y eliminar caracteres especiales excepto !?
    text = re.sub(r'[^a-z!?\s]', '', text.lower())
    lemmatizer = WordNetLemmatizer()
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]

    return ' '.join(tokens)
    
    
classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)
def classify_emotion(review):
    truncated_review = review[:720]
    return classifier(truncated_review)[0][0]
