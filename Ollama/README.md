# Ollama

## Pre-requisites:
- docker
- docker compose v2

## Getting up and running
```
docker compose up -d
```
This command will start both ollama and ollama-webui services in detached mode.

### Services
Ollama
- Image: ollama/ollama
- Ports: 11434:11434
- Volumes: ollama:/root/.ollama
- Restart Policy: unless-stopped
Ollama-WebUI
- Image: ghcr.io/open-webui/open-webui:main
- Ports: 8080:8080
- Extra Hosts: host.docker.internal:host-gateway
- Volumes: ollama-webui:/app/backend/data
- Restart Policy: unless-stopped


### Pull the images
Find the libray that you would like to pull from [Ollama library](https://ollama.com/library)
Assuming that you would like to pull llama3.1
1. Pull from Ollama UI via http://localhost:3000
2. Using docker exec to pull the image
```
docker exec -it ollama-docker-compose-ollama-1 ollama pull llama3.1
```
3. Using docker compose exec to pull the image
```
docker compose exec ollama ollama pull llama3.1
```

## Shutting down any old Docker containers
```
docker compose down
```

## Removing Ollama containers
docker system prune --all --force --volumes
