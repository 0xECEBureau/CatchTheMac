FROM python:3.11-slim

# Crée un utilisateur non-root
RUN useradd -m ctfuser

# Dépendances de base
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crée et utilise le dossier de travail
WORKDIR /app

# Copie le code
COPY app.py /app
COPY templates /app/templates
COPY static /app/static

# Donne les bons droits à l'utilisateur non-root
RUN chown -R ctfuser:ctfuser /app

# Installe Flask
RUN pip install --no-cache-dir flask

# Utilise l'utilisateur non-root
USER ctfuser

# Expose le port utilisé par Flask
EXPOSE 5000

# Lance l'application
CMD ["python", "app.py"]

