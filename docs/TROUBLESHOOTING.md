# Troubleshooting

## Common Issues

### Database Connection Errors

Check that PostgreSQL is running and accessible:
```bash
docker ps | grep postgres
```

### Service Not Starting

Check logs:
```bash
docker-compose logs <service-name>
```

### Migration Errors

Reset migrations:
```bash
python manage.py migrate --run-syncdb
```

## Health Checks

Run health check script:
```bash
bash scripts/health-check.sh
```
