# Streamify

A modern microservices-based streaming platform built with Django, Docker, and Kubernetes.

## Architecture

Streamify is built using a microservices architecture with the following services:

- **auth-service**: User authentication and authorization
- **stream-service**: Stream management and video processing
- **chat-service**: Real-time chat functionality via WebSockets
- **notification-service**: Email and push notifications

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- PostgreSQL 14+
- Redis 7+

### Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd streamify
```

2. Set up environment variables:
```bash
cp docker/env/.env.example docker/env/.env.dev
# Edit docker/env/.env.dev with your configuration
```

3. Start services:
```bash
# Full dev stack (all 4 Django services + Celery + infra)
make dev-up

# Or base only (postgres, redis, rabbitmq, auth-service, nginx)
make up-base
```

4. Run migrations:
```bash
make migrate-all
```

5. Access services:
- API Gateway: http://localhost:8000
- Auth Service: http://localhost:8001
- Stream Service: http://localhost:8002
- Chat Service: http://localhost:8003
- Notification Service: http://localhost:8004

## Docker Compose

| File | Purpose |
|------|--------|
| `docker/docker-compose.yml` | Base: postgres, redis, rabbitmq, auth-service, nginx (version 3.9, healthchecks, named volumes, `streamify-net`) |
| `docker/docker-compose.dev.yml` | Dev: all Django services + Celery, volume mount for hot-reload, exposed ports, `runserver`; use with `--profile dev` |
| `docker/docker-compose.prod.yml` | Prod: same services with gunicorn, no code mount, `restart: unless-stopped`, logging options |
| `docker/docker-compose.monitoring.yml` | Prometheus + Grafana; use with `--profile monitoring` |

- **Base only:** `make up-base` or `docker compose -f docker/docker-compose.yml up -d`
- **Full dev:** `make dev-up` (uses dev profile)
- **Prod:** `make prod-up`
- **With monitoring:** `make monitoring-up` (after base or dev is up)

## Project Structure

```
streamify/
├── services/          # Microservices
├── shared/            # Shared libraries and protobuf definitions
├── docker/            # Docker configurations
├── helm/              # Kubernetes Helm charts
├── monitoring/        # Monitoring stack (Prometheus, Grafana, ELK)
├── docs/              # Documentation
└── scripts/           # Utility scripts
```

## Development

See [DEVELOPMENT.md](docs/DEVELOPMENT.md) for detailed development guidelines.

## Deployment

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for deployment instructions.

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for contribution guidelines.

## License

See [LICENSE](LICENSE) for details.
