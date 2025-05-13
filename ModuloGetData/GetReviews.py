import requests
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from Preprocessing import clean_review , classify_emotion

load_dotenv()

username = os.getenv("MONGO_ROOT_USER")
password = os.getenv("MONGO_ROOT_PASSWORD")
db_name = os.getenv("MONGO_APP_DB")
host = os.getenv("MONGO_HOST")
port = os.getenv("MONGO_PORT", "27017")

client = MongoClient(f"mongodb://{username}:{password}@{host}:{port}/{db_name}?authSource={db_name}")


#client = MongoClient(
#    "mongodb://appuser:apppassword@mongodb:27017/moviesdb?authSource=moviesdb"
#)


db = client[os.getenv("MONGO_APP_DB", "moviesdb")]
reviews_collection = db.reviews


all_reviews = []
def get_reviews():
  #Extraer las reviews
  api_key = os.getenv('API_KEY')
  print("***  api_key=",api_key)

  #Diccionario con los generos y ids de las peliculas
  genres_url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=es-MX'
  genres_response = requests.get(genres_url)
  genres_data = genres_response.json()
  genres_dict = {genre['id']: genre['name'] for genre in genres_data['genres']}
  genres_dict

  all_movie_ids = []

  # URL para obtener las peliculas mejor calificadas
  base_url = "https://api.themoviedb.org/3"
  endpoint = "/movie/top_rated"  # o "/movie/popular"
  params = {
      "api_key": api_key,
  #    "language": "es-ES",
  #    "sort_by": "popularity.desc",
      "page": 1
  }

  #Obtener peliculas y reviews de varias páginas
  for page in range(1, 500):
      params["page"] = page
      # Realizamos solicitud GET
      response = requests.get(base_url + endpoint, params=params) 

      #Verificamos que la solicitud fue exitosa
      if response.status_code == 200:
          # Convertimos a un formato JSON
          movies = response.json()["results"]
          #Extraemos  titulo, genero, fecha de estreno, otros metadatos y agregamos a un diccionario el movie_id
          for movie in movies:  
            movie_id = movie['id']
            title = movie.get('title', 'Sin título')
            release_date = movie.get('release_date', '')
            vote_average = movie.get('vote_average', 0)
            genre_names = ', '.join([genres_dict.get(genre_id, 'Desconocido') for genre_id in movie.get('genre_ids', [])])
            all_movie_ids.append(movie_id)

            #Hacemos el request para extraer las reviews
            review_url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={api_key}"
            review_response =  requests.get(review_url)

            #Obtener los datos de la pelicula actual
            if review_response.status_code == 200:
              review_data = review_response.json()
              #Si review esta vacio continuamos
              if not review_data["results"]:
                continue
              #Agregamos a un diccionario todos nuestros datos 
              for review in review_data['results']:
                cleaned_review = clean_review(review.get('content', ''))
                emotion_review = classify_emotion(cleaned_review) 

                save_reviews({'movie_id': movie_id,
                                    'title': title,
                                    'release_date': release_date,
                                    'vote_average': vote_average,
                                    'genre_names': genre_names,
                                    'review': cleaned_review,
                                    'emotion': emotion_review})
            else:
              print(f"Error en página {movie_id}: {review_response.status_code}")

      else:
        print(f"Error en página {page}: {response.status_code}")


  print(f"IDs obtenidos: {len(all_movie_ids)}")
  print(f"Reviews obtenidos: {len(all_reviews)}")

  return all_reviews 


def save_reviews(review):
  reviews_collection.insert_one(review)
  print("Insertando en moviesdb: ", review)
get_reviews()


client.close()

print("*** FIN GetReviews ***")

