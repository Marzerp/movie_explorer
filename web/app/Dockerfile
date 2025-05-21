FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install pymongo  python-dotenv flask

CMD ["python", "-u", "generar_html.py"]
