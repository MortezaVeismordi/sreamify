# Chat Service

Real-time chat service for Streamify platform using WebSockets.

## Features

- Real-time messaging via WebSockets
- Chat rooms for streams
- Message history
- User presence tracking

## API Endpoints

- `GET /api/chat/rooms/` - List chat rooms
- `POST /api/chat/rooms/` - Create chat room
- `GET /api/chat/messages/` - Get messages
- `POST /api/chat/messages/` - Send message
- `WS /ws/chat/{room_id}/` - WebSocket connection

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
