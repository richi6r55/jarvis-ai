# Docker Setup Guide

## Quick Start with Docker

### Prerequisites
- Docker installed (https://www.docker.com/products/docker-desktop)
- Docker Compose installed
- API keys ready

### Build and Run

#### 1. Create .env file
```bash
cp .env.example .env
# Edit .env with your API keys
```

#### 2. Build images
```bash
docker-compose build
```

#### 3. Start services
```bash
docker-compose up -d
```

#### 4. Check status
```bash
docker-compose ps
```

Output should show:
```
CONTAINER ID   IMAGE                 STATUS
...            jarvis-backend        Up (healthy)
...            jarvis-frontend       Up (healthy)
```

#### 5. Access application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### View Logs

```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Rebuild After Code Changes

```bash
# Stop services
docker-compose down

# Rebuild images
docker-compose build --no-cache

# Start again
docker-compose up -d
```

## Troubleshooting

### Service won't start
```bash
# Check logs
docker-compose logs backend

# Common issues:
# 1. Port already in use: Change port in docker-compose.yml
# 2. Missing .env file: cp .env.example .env
# 3. API keys not set: Edit .env with real keys
```

### Container keeps restarting
```bash
# View detailed logs
docker-compose logs --tail=50 backend

# Stop and inspect
docker-compose stop
docker-compose logs backend
```

### Health check failing
```bash
# Check if services are actually running
docker-compose exec backend curl http://localhost:8000/health

# View service logs
docker-compose logs backend
```

## Advanced Usage

### Run specific service
```bash
docker-compose up -d backend  # Only backend
docker-compose up -d frontend # Only frontend
```

### Execute commands in container
```bash
# Run Python command in backend
docker-compose exec backend python -c "print('hello')"

# Install package
docker-compose exec backend pip install package-name
```

### Resource limits
Edit docker-compose.yml to add:
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

### Persistent data
Volumes are configured for:
- `/app/logs` - Application logs
- `/app/screenshots` - Screenshots from browser automation

They persist even after container stops.

## Production Deployment

For production, consider:
1. Using environment-specific compose files
2. Adding reverse proxy (nginx)
3. Setting up SSL/TLS
4. Using Docker secrets for sensitive data
5. Implementing container orchestration (Kubernetes)

See DEPLOYMENT.md for more details.
