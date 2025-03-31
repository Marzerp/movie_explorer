#Extraer las reviews

api_key = "https://www.themoviedb.org/documentation/api"

#Diccionario con los generos y ids de las peliculas
genres_url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=es-MX'
genres_response = requests.get(genres_url)
genres_data = genres_response.json()
genres_dict = {genre['id']: genre['name'] for genre in genres_data['genres']}
genres_dict

all_movie_ids = []
all_reviews = []

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
        # Lo convertimos a un formato JSON
        movies = response.json()["results"]
        #Extraemos  titulo, genero, fecha de estreno y otros metadatos y 
        # agregamos a un diccionario el movie_id
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
              all_reviews.append({'movie_id': movie_id,
                                  'title': title,
                                  'release_date': release_date,
                                  'vote_average': vote_average,
                                  'genre_names': genre_names,
                                  'review': review.get('content', '') })
          else:
            print(f"Error en página {movie_id}: {review_response.status_code}")

    else:
      print(f"Error en página {page}: {response.status_code}")


print(f"IDs obtenidos: {len(all_movie_ids)}")
print(f"Reviews obtenidos: {len(all_reviews)}")
