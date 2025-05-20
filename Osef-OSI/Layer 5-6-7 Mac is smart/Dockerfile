FROM python:3.11-slim

# ── dépendances système pour Chrome headless ──────────────────────────────
RUN apt-get update \
 && apt-get install -y --no-install-recommends chromium \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copie des sources et du flag
COPY sources/ ./sources/
COPY flag.txt ./flag.txt

# Dépendances Python
COPY sources/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Le bot a besoin d'autoriser l'accès réseau sortant (si webhook)
EXPOSE 5000

# Script de lancement (app + bot)
RUN chmod +x sources/run.sh
CMD ["/app/sources/run.sh"]