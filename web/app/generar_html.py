from pymongo import MongoClient
from flask import Flask, render_template_string, redirect, url_for, request
import os
import sys

from dotenv import load_dotenv
from pymongo import MongoClient

sys.stdout.reconfigure(line_buffering=True)  

app = Flask(__name__)


load_dotenv()

username = os.getenv("MONGO_APP_USER")
password = os.getenv("MONGO_APP_PASSWORD")
db_name = os.getenv("MONGO_APP_DB")
host = os.getenv("MONGO_HOST")
port = os.getenv("MONGO_PORT", "27017")

client = MongoClient(f"mongodb://{username}:{password}@{host}:{port}/{db_name}?authSource={db_name}")

print("=== client=", client, flush=True)

db = client[os.getenv("MONGO_APP_DB", "moviesdb")]
reviews_collection = db.reviews

@app.route('/')
def home():
    html = """
    <html>
    <body>
    """

    html += f"<h1>Movie Explorer</h1>"

    html += """
        <form action="/generar_reporte" method="get">
        
            <label for="year">Release year:</label>
            <input type="number" id="year" name="year" placeholder="2025"><br>
                        
            <label for="keyWord">Key Word in Movie Title:</label>
            <input type="search" id="keyWord" name="keyWord" placeholder="Enter a key word"><br>
                     
            <label for="numPage">Number of movies to display:</label>
            <input type="number" id="numPage" name="numPage" placeholder="10"><br>
            
            <p> Search by Emotions:
            <label for="joy">
              <input type="checkbox" id="joy" name="joy" value="true"> Joy
            </label>
            <label for="anger">
              <input type="checkbox" id="anger" name="anger" value="true"> Anger
            </label>
            <label for="sadness">
              <input type="checkbox" id="sadness" name="sadness" value="true"> Sadness
            </label>
            <label for="disgust">
              <input type="checkbox" id="disgust" name="disgust" value="true"> Disgust
            </label>
            <label for="surprise">
              <input type="checkbox" id="surprise" name="surprise" value="true"> Surprise
            </label>
            <label for="neutral">
              <input type="checkbox" id="neutral" name="neutral" value="true"> Neutral
            </label>
            <label for="fear">
              <input type="checkbox" id="fear" name="fear" value="true"> Fear
            </label><br>
            </p>
            
            <p>
            <label for="genre">Filter by Genre:</label>
            <select id="genre" name="genre">
                <option value="">All Genres</option>
                <option value="Crimen">Crime</option>
                <option value="Historia">History</option>
                <option value="Familia">Family</option>
                <option value="Acción">Action</option>
                <option value="Drama">Drama</option>
                <option value="Película de TV">TV Movie</option>
                <option value="Misterio">Mistery</option>
                <option value="Suspense">Suspense</option>
                <option value="Comedia">Comedy</option>
                <option value="Bélica">Military</option>
                <option value="Música">Music</option>
                <option value="Western">Western</option>
                <option value="Animación">Animation</option>
                <option value="Romance">Romance</option>
                <option value="Aventura">Adventure</option>
                <option value="Fantasía">Fantasy</option>
                <option value="Terror">Terror</option>
                <option value="Ciencia ficción">SciFi</option>
            </select><br>
            </p>
            
            <label for="fullInfo">
              <input type="checkbox" id="fullInfo" name="fullInfo" value="true"> Display Full Info
            </label><br>
    
            <button type="submit">Search</button>
        </form>
    </body>
    </html>
    """
    return html

@app.route('/generar_reporte')
def generar_reporte():
    def title_unique(query):
      pipeline = [
  
      {"$match": query}, 
    
      # Agrupar por título y tomar el primer registro (o el más reciente)
      {"$group": {
          "_id": "$title",  # Agrupa por título
          "poster_url": {"$first": "$poster_url"}, 
          "release_date": {"$first": "$release_date"},  # Toma la primera fecha
          "emotion": {"$first": "$emotion"}  # Toma el primer resultado de emoción
                                             
      }},
    
      # Limitar resultados 
      {"$limit": numPage}
      ]

      movies = list(reviews_collection.aggregate(pipeline))
      print(movies)
      return movies
    
    print("=== INICIO GENERAR_REPORTE ===", flush=True)
    
    # Obtener parámetros
    year_arg = request.args.get('year')
    keyWord = request.args.get('keyWord')
    numPage_arg = request.args.get('numPage')
    fullInfo_arg = request.args.get('fullInfo')
    joy_arg = request.args.get('joy')
    anger_arg = request.args.get('anger')
    sadness_arg = request.args.get('sadness')
    disgust_arg = request.args.get('disgust')
    surprise_arg = request.args.get('surprise')
    neutral_arg = request.args.get('neutral')
    fear_arg = request.args.get('fear')

    genre_arg = request.args.get('genre')
    
    genre_arg = request.args.get('genre')
    
    numPage = int(numPage_arg) if numPage_arg else 10
    year = int(year_arg) if year_arg else None
    fullInfo = True if fullInfo_arg=="true" else False
    
    active_emotions = []
    if joy_arg=="true":
      active_emotions.append("joy")
    if anger_arg=="true":
      active_emotions.append("anger")
    if sadness_arg=="true":
      active_emotions.append("sadness")
    if disgust_arg=="true":
      active_emotions.append("disgust")
    if surprise_arg=="true":
      active_emotions.append("surprise")
    if neutral_arg=="true":
      active_emotions.append("neutral")
    if fear_arg=="true":
      active_emotions.append("fear")

    n = reviews_collection.count_documents({})
    print(f"Total documentos: {n}", flush=True)
     
    n = reviews_collection.count_documents({})
    try:
        query = {}
        if year:
           query["release_date"] = {"$regex": f"^{year}"}  
        if keyWord:
            query["title"] = {"$regex": keyWord, "$options": "i"} 
        if active_emotions:
            query["emotion.label"] = {"$in": active_emotions}
        if genre_arg != "":
            query["genre_names"] = {"$regex": f"\\b{genre_arg}\\b", "$options": "i"}
      
  
        if fullInfo:
            movies = list(reviews_collection.find(query).limit(numPage))
        else:
            movies = title_unique(query)

        num = len(movies)
        print(f"Number of movies found: {num}", flush=True)
        
        html = """
            <html>
            <body>
            <h1>Search Results:</h1>
            """
        
        if year:
            html += f"<h2>Release year: {year}</h2>"
        
        html += f"Found {num} of {n}<br><br><ul>"
        
        for movie in movies:
            html += "<li>"
            poster_url = movie.get("poster_url", None)
            if poster_url:
                html += f"<img src='{poster_url}' alt='Poster' style='height: 100px;'><br>"
            if fullInfo:
                html += f"{movie['title']} - {movie['release_date']} - genre:{movie['genre_names']} - emotion: {movie['emotion']}</li>"
            else:
                html += f"{movie['_id']} - {movie['release_date']} </li>"
                    
        html += """
            </ul>
            <a href="/"><button>Back</button></a>
            """
        html += f"(movies found: {num})</body></html>"
        return html
        
    except Exception as e:
        print(f"\n*** ERROR: {str(e)} ***", flush=True)
        return f"Error: {str(e)}", 500
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
