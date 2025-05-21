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
    html += f"<h1>Peliculas en la BD: {n}</h1>"
    html += """
        <form action="/generar_reporte" method="get">
            <label for="edad">Filtrar por edad:</label>
            <input type="number" id="edad" name="edad" placeholder="Por ejemplo: 40">
            <button type="submit">Generar Reporte</button>
        </form>
    </body>
    </html>
    """
    return html

@app.route('/generar_reporte')
def generar_reporte():
    print("=== INICIO GENERAR_REPORTE ===", flush=True)
    
    # Obtener parámetro de edad (si existe)
    edad_filtro = request.args.get('edad')
    
    try:
        db = client["empresa"]
        
        # Construir query basado en si hay filtro de edad
#        query = {} if not edad_filtro else {"edad": int(edad_filtro)}
        query = {}        
        empleados = list(db["empleados"].find(query))
        print(f"Empleados encontrados: {len(empleados)}", flush=True)
        
        html = """
            <html>
            <body>
            <h1>Reporte de Peliculas</h1>
            """
        
        if edad_filtro:
            html += f"<h2>Filtrado por edad: {edad_filtro} años</h2>"
        
        html += """
            <ul>
            """
        for emp in empleados:
            html += f"<li>{emp['nombre']} - {emp['edad']} años</li>"
        
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
