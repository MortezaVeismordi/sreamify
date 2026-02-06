# Notification Service

Notification service for Streamify platform with email and push notifications.

## Features

- Email notifications
- Push notifications
- Notification preferences
- Celery task queue for async processing

## API Endpoints

- `GET /api/notifications/` - List notifications
- `POST /api/notifications/` - Create notification
- `PUT /api/notifications/{id}/read/` - Mark as read
- `DELETE /api/notifications/{id}/` - Delete notification

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start Celery worker
celery -A config.celery worker --loglevel=info

# Run server
python manage.py runserver
```

## Testing

```bash
pytest
```
