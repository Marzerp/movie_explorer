from pymongo import MongoClient
from flask import Flask, render_template_string, redirect, url_for, request, session

from flask import send_from_directory

import os
import sys
import random 
from dotenv import load_dotenv


from PIL import Image, ImageDraw, ImageFont
import io
import base64


sys.stdout.reconfigure(line_buffering=True)  

app = Flask(__name__)
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes

#####################
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)
###########################

load_dotenv()


load_dotenv()

username = os.getenv("MONGO_APP_USER")
password = os.getenv("MONGO_APP_PASSWORD")
db_name = os.getenv("MONGO_APP_DB")
host = os.getenv("MONGO_HOST")
port = os.getenv("MONGO_PORT", "27017")

app.secret_key = os.getenv("FLASK_CAPTCHA_KEY") 


client = MongoClient(f"mongodb://{username}:{password}@{host}:{port}/{db_name}?authSource={db_name}")

print("=== client=", client, flush=True)

db = client[os.getenv("MONGO_APP_DB", "moviesdb")]
reviews_collection = db.reviews

<<<<<<< Updated upstream

=======
##########################################
>>>>>>> Stashed changes
# Configuración de CAPTCHA de imágenes
CAPTCHA_IMAGES_DIR = "captcha_images"
os.makedirs(CAPTCHA_IMAGES_DIR, exist_ok=True)

def generate_image_captcha():
    # Generar texto aleatorio
    text = ''.join(random.choices('ABCDEFGHJKLMNPQRSTUVWXYZ23456789', k=6))
    
    # Crear imagen
    image = Image.new('RGB', (200, 80), color=(240, 240, 240))
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    # Dibujar texto con distorsión
    for i, char in enumerate(text):
        draw.text((20 + i*30, 20), char, font=font, fill=(random.randint(0, 150), random.randint(0, 150), random.randint(0, 150)))
    
    # Añadir ruido
    for _ in range(5000):
        draw.point((random.randint(0, 200), random.randint(0, 80)), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return text, img_str
    
<<<<<<< Updated upstream

=======
    
#########################################
>>>>>>> Stashed changes

@app.route('/')
def home():
    captcha_text, captcha_image = generate_image_captcha()
    session['captcha_text'] = captcha_text
    
    
    html = """
    <html>
    <body>
    """

    html += f"<h1>Movie Explorer</h1>"

    html += """
        <form action="/generar_reporte" method="post">
        
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
            
            <!-- Checkbox para información completa -->
            <label for="fullInfo">
              <input type="checkbox" id="fullInfo" name="fullInfo" value="true"> Display Full Info
            </label><br>
            <br>
            <div style="margin: 10px 0; padding: 10px; background: #f0f0f0;">
            """
    html += f"<label>Type the characters you see in the picture</label>"
    html += f'<img src="data:image/png;base64,{captcha_image}" alt="CAPTCHA">'
    html += """
            <input type="text" name="captcha" required>
            </div>
            <button type="submit">Search</button>
            </form>
            </body>
            </html>
            """.format(captcha_image=captcha_image)
    return html

@app.route('/generar_reporte', methods=['POST'])
def generar_reporte():

    user_answer = request.form.get('captcha', '').upper()
    correct_answer = session.get('captcha_text', '').upper()
    
    if user_answer is None or user_answer != correct_answer:
       return """
        <html><body>
        <h2>Incorrect CAPTCHA. Please try again.</h2>
        <a href="/"><button>Back</button></a>
        </body></html>
        """, 400
    session.pop('captcha_text', None)
    
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
      return movies
    
    print("=== INICIO GENERAR_REPORTE ===", flush=True)
    
    # Obtener parámetros
    year_arg = request.form.get('year')
    keyWord = request.form.get('keyWord')
    numPage_arg = request.form.get('numPage')
    fullInfo_arg = request.form.get('fullInfo')
    joy_arg = request.form.get('joy')
    anger_arg = request.form.get('anger')
    sadness_arg = request.form.get('sadness')
    disgust_arg = request.form.get('disgust')
    surprise_arg = request.form.get('surprise')
    neutral_arg = request.form.get('neutral')
    fear_arg = request.form.get('fear')

    genre_arg = request.form.get('genre')
    
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
        return html
        
    except Exception as e:
        print(f"\n*** ERROR: {str(e)} ***", flush=True)
        return f"Error: {str(e)}", 500
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
