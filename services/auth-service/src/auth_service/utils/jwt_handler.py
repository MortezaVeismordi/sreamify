import jwt
from datetime import datetime, timedelta
from django.conf import settings


def get_refresh_token_lifetime():
    return getattr(settings, "JWT_REFRESH_TOKEN_LIFETIME", 86400)


def generate_access_token(user_id):
    exp = datetime.utcnow() + timedelta(seconds=settings.JWT_ACCESS_TOKEN_LIFETIME)
    payload = {
        "user_id": user_id,
        "exp": exp,
        "iat": datetime.utcnow(),
        "type": "access",
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def generate_refresh_token(user_id):
    """Returns (token_str, expires_at_datetime)"""
    lifetime = get_refresh_token_lifetime()
    exp = datetime.utcnow() + timedelta(seconds=lifetime)
    payload = {
        "user_id": user_id,
        "exp": exp,
        "iat": datetime.utcnow(),
        "type": "refresh",
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token, exp


def verify_token(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
