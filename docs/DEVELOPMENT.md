# Development Guide

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL 14+
- Redis 7+

## Setup

1. Clone the repository
2. Copy environment files: `cp docker/env/.env.example docker/env/.env.dev`
3. Start services: `make dev-up`
4. Run migrations: `make migrate-all`

## Running Tests

```bash
pytest
```

## Code Style

- Use Black for code formatting
- Use isort for import sorting
- Follow PEP 8 guidelines
- Write tests for all new features

## Git Workflow

1. Create feature branch from `develop`
2. Make changes and commit
3. Push and create pull request
4. Code review and merge
