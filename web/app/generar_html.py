from pymongo import MongoClient
from flask import Flask, render_template_string, redirect, url_for, request
import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient

sys.stdout.reconfigure(line_buffering=True)  # Forzar flush inmediato

app = Flask(__name__)

# Configuración MongoDB
#client = MongoClient(
#    "mongodb://admin:admin123@base_mongo:27017/",
#    authSource="admin"
#)

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
n = reviews_collection.count_documents({})
print(f"Total documentos: {n}", flush=True)

@app.route('/')
def home():
    html = """
    <html>
    <body>
    """
    html += f"<h1>Movie Explorer (total movies: {n})</h1>"
    html += """
        <form action="/generar_reporte" method="get">
            <label for="year">Release year:</label>
            <input type="number" id="year" name="year" placeholder="2025">
            <label for="numPage">Number of movies to display:</label>
            <input type="number" id="numPage" name="numPage" placeholder="10">
            <button type="submit">Search</button>
        </form>
    </body>
    </html>
    """
    return html

@app.route('/generar_reporte')
def generar_reporte():
    print("=== INICIO GENERAR_REPORTE ===", flush=True)
    
    # Obtener parámetros
    year_arg = request.args.get('year')
    numPage_arg = request.args.get('numPage')
    
    # Establecer valores por defecto
    numPage = int(numPage_arg) if numPage_arg else 10
    year = int(year_arg) if year_arg else None
    
    try:
        # Construir query basado en el año si se especificó
        query = {"release_date": {"$regex": f"^{year}"}} if year else {}
        
        # Obtener las películas y convertirlas a lista (limitando a numPage)
        movies = list(reviews_collection.find(query).limit(numPage))
        
        print(f"Number of movies found: {len(movies)}", flush=True)
        
        html = """
            <html>
            <body>
            <h1>Search Results:</h1>
            """
        
        if year:
            html += f"<h2>Release year: {year}</h2>"
        
        html += "<ul>"
        
        for movie in movies:
            html += f"<li>{movie['title']} - {movie['release_date']} - emotion:{movie['emotion']} </li>"
        
        html += """
            </ul>
            <a href="/"><button>Volver</button></a>
            </body>
            </html>
            """
        return html
        
    except Exception as e:
        print(f"\n*** ERROR: {str(e)} ***", flush=True)
        return f"Error: {str(e)}", 500
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
