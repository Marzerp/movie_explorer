FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*
    
WORKDIR /app
COPY . .

RUN pip install pymongo  python-dotenv flask
RUN pip install --no-cache-dir Pillow pymongo python-dotenv flask


CMD ["python", "-u", "generar_html.py"]
