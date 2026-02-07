# Auth Service (Streamify) 🔐

A high-performance, industry-standard authentication service built with Django 5 and Django REST Framework. This service implements advanced security patterns often required in Fintech, SaaS, and Streaming platforms.

## ✨ Security Highlights

- **Refresh Token Rotation**: Every time a token is refreshed, a new `refresh_token` is issued and the old one is immediately invalidated to prevent session hijacking.
- **Server-side Revocation (Blacklist)**: Implements a database-backed blacklist for `refresh_tokens`. This allows for features like "Logout from all devices" and immediate token invalidation.
- **HttpOnly Secure Cookies**: Refresh tokens are served exclusively via `HttpOnly`, `SameSite=Strict` cookies. This mitigates XSS and CSRF risks and ensures tokens never touch the frontend JavaScript's memory.
- **Cookie-based Refresh Logic**: The `/tokens/refresh/` endpoint is strictly cookie-based. It does not accept tokens in the request body, maintaining a clean and secure authentication flow.
- **Password Reset Flow**: Implements a secure, email-based password recovery system using Django's cryptographically signed tokens and base64-encoded UIDs.
- **Smart Rate Limiting (Brute-force protection)**: Sensitive endpoints like `login`, `register`, and `refresh` are protected by `ScopedRateThrottling` (10 requests/minute per client).
- **Custom User Model**: Uses `email` as the primary identifier with a robust `CustomUserManager`.

## 🛠 Tech Stack

- **Framework**: Django 5.x, Django REST Framework
- **Auth**: JWT (PyJWT), HttpOnly Cookies
- **Database**: PostgreSQL (Production-ready)
- **Cache**: Redis (via `django-redis` for potential session/throttle storage)
- **Architecture**: Domain-Driven Design (DDD) principles with separated apps for `users` and `tokens`.

## 🚀 Key Endpoints

| Endpoint | Method | Security Level | Purpose |
| :--- | :--- | :--- | :--- |
| `/api/users/register/` | POST | Public | Creates a new user & sets initial cookie. |
| `/api/users/login/` | POST | Public | Authenticates user & sets HttpOnly cookie. |
| `/api/tokens/refresh/` | POST | Cookie | Rotates refresh token & issues new access token. |
| `/api/users/me/` | GET/PUT | Authenticated | View or partially update profile data. |
| `/api/users/logout/` | POST | AllowAny | Revokes server-side token & clears cookie. |

## 🧪 Testing

The authentication flow is covered with 100% E2E test coverage for success paths and security edge cases.

```bash
# Run tests
python manage.py test auth_service.apps.users auth_service.apps.tokens
```
