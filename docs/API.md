# API Documentation

## Authentication

All authenticated endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

## Endpoints

### Auth Service

- `POST /api/users/register/` - Register new user
- `POST /api/users/login/` - Login and get tokens
- `GET /api/users/me/` - Get current user profile

### Stream Service

- `GET /api/streams/` - List streams
- `POST /api/streams/` - Create stream
- `GET /api/streams/{id}/` - Get stream details

### Chat Service

- `GET /api/chat/rooms/` - List chat rooms
- `POST /api/chat/messages/` - Send message
- `WS /ws/chat/{room_id}/` - WebSocket connection

### Notification Service

- `GET /api/notifications/` - List notifications
- `POST /api/notifications/` - Create notification
