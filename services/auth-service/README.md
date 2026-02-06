# Auth Service

Authentication and authorization service for Streamify platform.

## Features

- User registration and login
- JWT token generation and validation
- Token refresh mechanism
- Password reset functionality
- User profile management

## API Endpoints

- `POST /api/users/register/` - Register a new user
- `POST /api/users/login/` - Login and get tokens
- `POST /api/tokens/refresh/` - Refresh access token
- `POST /api/tokens/verify/` - Verify token validity
- `GET /api/users/me/` - Get current user profile
- `PUT /api/users/me/` - Update current user profile

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
