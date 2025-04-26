# Challenges Web

## Build Docker

```powershell
# Build and push challenge 0
docker build -t tristanqtn/chall_0 "./00 - Warm Up/source" --no-cache
docker push tristanqtn/chall_0

# Build and push challenge 1
docker build -t tristanqtn/chall_1 "./01 - Generateur Super Secure/source" --no-cache
docker push tristanqtn/chall_1

# Build and push challenge 2
docker build -t tristanqtn/chall_2 "./02 - Generateur Vraiment Super Secure/source" --no-cache
docker push tristanqtn/chall_2

# Build and push challenge 3
docker build -t tristanqtn/chall_3 "./03 - Generateur Vraiment Super Mega Secure/source" --no-cache
docker push tristanqtn/chall_3
```

# Infra

L'infrastructre est composée de 4 containers Docker. Ces conteneurs sont hébergés sur mon DockerHub: https://hub.docker.com/u/tristanqtn

```bash
docker compose up -d
```
