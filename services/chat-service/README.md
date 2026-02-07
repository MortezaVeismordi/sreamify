# Chat Service

Real-time chat service for Streamify platform using WebSockets.

## Features

- Real-time messaging via WebSockets
- Chat rooms for streams
- Message history
- **WebSocket authentication via JWT access token** (query string or header), with internal verification to auth-service

## WebSocket authentication

Connect with the **access token** (from auth-service login) so the chat service can verify the user:

- **URL:** `ws://chat-service-domain/ws/chat/<room_id>/?token=<access_token>`
- Token is read from the `token` query parameter (or `Authorization: Bearer <token>` header).
- Only **access tokens** are accepted (not refresh tokens).
- Chat-service calls auth-service `POST /api/tokens/verify-bearer/` to validate the token; on success, `scope['user']` is set (id, email, username) and the connection is accepted; otherwise the connection is closed with code `4001`.
- In production use **WSS** (HTTPS) so the token in the query string stays secure.
- Optional: verify result is cached in Redis (`WS_JWT_VERIFY_CACHE_TTL` seconds) to reduce auth-service calls.

## API Endpoints

- `GET /api/chat/rooms/` - List chat rooms
- `POST /api/chat/rooms/` - Create chat room
- `GET /api/chat/messages/` - Get messages
- `POST /api/chat/messages/` - Send message
- `WS /ws/chat/{room_id}/?token=<access_token>` - WebSocket connection (authenticated)

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
