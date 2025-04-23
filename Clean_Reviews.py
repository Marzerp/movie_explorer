"""
Script para cargar y preprocesar reseñas de películas extraídas desde TMDb.
Realiza limpieza de texto, elimina ruido textual y traduce de emojis.
"""

import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Descarga de recursos necesarios de NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

# Inicializamos el stemmer
stemmer = PorterStemmer()

# 1. Cargar el archivo CSV
df = pd.read_csv('data/all_reviews.csv')

# 2. Convertir 'release_date' al formato de fecha
df['release_date'] = pd.to_datetime(df['release_date'])

# 3. Función para preprocesar el texto de las reseñas
def preprocess_text(text):
    """
    Limpia el texto de una reseña: remueve menciones, URLs, hashtags, emojis,
    signos de puntuación, números, stopwords y aplica stemming.
    """
    if not isinstance(text, str):
        return ""
    
    # Reemplazar emojis por su nombre (por ejemplo, 😊 -> :smiling_face:)
    def translate_emojis(sentence):
        words = sentence.split()
        translated = []
        for word in words:
            if any(emoji.is_emoji(c) for c in word):
                translated.append(emoji.demojize(word))
            else:
                translated.append(word)
        return " ".join(translated)

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

# 4. Aplicar limpieza a las reseñas
df['clean_review'] = df['review'].apply(preprocess_text)

# 5. Guardar el nuevo CSV con las reseñas limpias
df.to_csv('data/cleaned_reviews.csv', index=False)

print("Limpieza completa, archivo guardado como 'data/cleaned_reviews.csv'")
