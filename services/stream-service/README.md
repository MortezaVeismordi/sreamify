# Stream Service

Stream management and video processing service for Streamify platform.

## Features

- Stream creation and management
- Video upload and processing
- Stream categories
- Stream search and filtering
- Stream statistics

## API Endpoints

- `GET /api/streams/` - List all streams
- `POST /api/streams/` - Create a new stream
- `GET /api/streams/{id}/` - Get stream details
- `PUT /api/streams/{id}/` - Update stream
- `DELETE /api/streams/{id}/` - Delete stream
- `GET /api/categories/` - List categories
- `POST /api/categories/` - Create category

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Run server
python manage.py runserver
```

## Testing

```bash
pytest
```
