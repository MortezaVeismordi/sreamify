# API Documentation

## Authentication

All authenticated endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

## Endpoints

### Auth Service

- `POST /api/users/register/` - Register new user
- `POST /api/users/login/` - Login and get tokens (returns `access_token`, `refresh_token`)
- `GET /api/users/me/` - Get current user profile
- `POST /api/tokens/verify/` - Verify token (body: `{"token": "..."}`)
- `GET/POST /api/tokens/verify-bearer/` - Verify Bearer token; returns user info (used internally by chat-service for WebSocket auth)

### Stream Service

- `GET /api/streams/` - List streams
- `POST /api/streams/` - Create stream
- `GET /api/streams/{id}/` - Get stream details

### Chat Service

- `GET /api/chat/rooms/` - List chat rooms
- `POST /api/chat/messages/` - Send message
- `WS /ws/chat/{room_id}/?token=<access_token>` - WebSocket connection (authenticated). Token can also be sent as `Authorization: Bearer <token>`. Only access tokens are accepted; chat-service verifies with auth-service. Use WSS in production.

### Notification Service

- `GET /api/notifications/` - List notifications
- `POST /api/notifications/` - Create notification
