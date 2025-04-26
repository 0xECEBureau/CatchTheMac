# Utiliser une image Python officielle
FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier du serveur dans le conteneur
COPY simple_tcp_server.py .

# Exposer le port 5000
EXPOSE 5000

# Lancer le serveur TCP
CMD ["python3", "simple_tcp_server.py"]
