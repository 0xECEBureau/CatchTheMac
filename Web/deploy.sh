#!/bin/bash
# This script deploys the web challenges on server and opens the necessary ports
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

PORT1=8000
PORT2=8001
PORT3=8002
PORT4=8003

echo "Allowing traffic on port ${PORT1}/tcp..."
sudo ufw allow ${PORT1}/tcp

echo "Allowing traffic on port ${PORT2}/tcp..."
sudo ufw allow ${PORT2}/tcp

echo "Allowing traffic on port ${PORT3}/tcp..."
sudo ufw allow ${PORT3}/tcp

echo "Allowing traffic on port ${PORT4}/tcp..."
sudo ufw allow ${PORT4}/tcp

echo "Starting Docker containers..."
docker compose up -d

echo "Deployment complete."