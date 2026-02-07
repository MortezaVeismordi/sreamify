"""
WebSocket JWT auth middleware.
Runs on connect: extracts token from query_string (?token=...) or headers (Authorization: Bearer),
verifies with auth-service (only access_token), sets scope["user"] or closes with 4001.
Optional Redis cache for verify result to reduce auth-service calls.
"""
import logging
from urllib.parse import parse_qs

import httpx
from django.conf import settings

logger = logging.getLogger(__name__)

# Close code for "unauthorized" (private use range)
WS_CLOSE_UNAUTHORIZED = 4001


def _get_token_from_scope(scope):
    """Extract JWT from scope['query_string'] (token=...) or scope['headers'] (Authorization: Bearer)."""
    token = None
    query_string = scope.get("query_string") or b""
    if query_string:
        qs = parse_qs(query_string.decode("utf-8"))
        tokens = qs.get("token", [])
        if tokens:
            token = tokens[0].strip()
    if not token:
        for name, value in scope.get("headers") or []:
            if name.lower() == b"authorization" and value.startswith(b"Bearer "):
                token = value[7:].decode("utf-8").strip()
                break
    return token


async def _verify_token_with_auth_service(token):
    """Call auth-service verify-bearer endpoint. Returns (user_dict, None) or (None, error_message)."""
    url = getattr(settings, "AUTH_SERVICE_VERIFY_URL", "http://auth-service:8000/api/tokens/verify-bearer/")
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.post(
                url,
                json={"token": token},
                headers={"Authorization": f"Bearer {token}"},
            )
    except Exception as e:
        logger.warning("Auth-service verify request failed: %s", e)
        return None, "Auth service unavailable"
    if r.status_code == 200:
        data = r.json()
        if data.get("valid") and "user_id" in data:
            return {
                "id": data["user_id"],
                "email": data.get("email", ""),
                "username": data.get("username", ""),
                "is_staff": data.get("is_staff", False),
                "is_streamer": data.get("is_streamer", False),
            }, None
        return None, "Invalid response"
    return None, r.json().get("error", "Unauthorized") or f"HTTP {r.status_code}"


async def _get_cached_user(token):
    """Return cached user dict if WS_JWT_VERIFY_CACHE_TTL > 0 and Redis available."""
    ttl = getattr(settings, "WS_JWT_VERIFY_CACHE_TTL", 0)
    if ttl <= 0:
        return None
    try:
        from django.core.cache import cache
        cache_key = f"ws_jwt:{token[:32]}"
        return cache.get(cache_key)
    except Exception:
        return None


def _set_cached_user(token, user_dict):
    """Cache user dict for WS_JWT_VERIFY_CACHE_TTL seconds."""
    ttl = getattr(settings, "WS_JWT_VERIFY_CACHE_TTL", 0)
    if ttl <= 0:
        return
    try:
        from django.core.cache import cache
        cache_key = f"ws_jwt:{token[:32]}"
        cache.set(cache_key, user_dict, timeout=ttl)
    except Exception:
        pass


class JWTAuthMiddleware:
    """
    ASGI middleware that validates JWT on WebSocket connect and sets scope['user'].
    Rejects with close code 4001 if token missing or invalid (only access_token accepted).
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "websocket":
            await self.app(scope, receive, send)
            return

        token = _get_token_from_scope(scope)
        if not token:
            await send({"type": "websocket.close", "code": WS_CLOSE_UNAUTHORIZED, "reason": "Missing token"})
            return

        user_dict = await _get_cached_user(token)
        if user_dict is None:
            user_dict, err = await _verify_token_with_auth_service(token)
            if err:
                await send({"type": "websocket.close", "code": WS_CLOSE_UNAUTHORIZED, "reason": err})
                return
            _set_cached_user(token, user_dict)

        scope["user"] = user_dict

        # Pass through to the application (consumer)
        await self.app(scope, receive, send)
