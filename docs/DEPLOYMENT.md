# Deployment Guide

## Production Deployment

### Using Docker Compose

```bash
docker-compose -f docker/docker-compose.yml -f docker/docker-compose.prod.yml up -d
```

### Using Kubernetes

```bash
helm install streamify ./helm --values ./helm/values-prod.yaml
```

## Environment Variables

Set the following environment variables in production:

- `SECRET_KEY`
- `JWT_SECRET_KEY`
- `DATABASE_URL`
- `REDIS_URL`
- `ALLOWED_HOSTS`

## Monitoring

- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000
- Kibana: http://localhost:5601
