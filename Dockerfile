# Usa la imagen oficial de MongoDB
FROM mongo:7.0

RUN python -m nltk.downloader punkt stopwords wordnet

# Opcional: Copia scripts de inicialización
COPY ./mongo-init.js /docker-entrypoint-initdb.d/

# Puerto expuesto (por defecto MongoDB usa 27017)
EXPOSE 27017

# Comando por defecto (inicia MongoDB)
CMD ["mongod", "--bind_ip_all", "--auth"]  # Permite conexiones externas
