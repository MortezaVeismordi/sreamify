from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from django.contrib.auth import get_user_model
from .models import RefreshToken
from .serializers import TokenVerifySerializer
from auth_service.utils.jwt_handler import generate_access_token, generate_refresh_token, verify_token

User = get_user_model()


def _set_refresh_cookie(response, token):
    cookie_max_age = getattr(settings, "JWT_REFRESH_TOKEN_LIFETIME", 86400)
    response.set_cookie(
        key="refresh_token",
        value=token,
        max_age=cookie_max_age,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="Strict",
    )


@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([ScopedRateThrottle])
def refresh_token(request):
    request.throttle_scope = "auth"
    token = request.COOKIES.get("refresh_token")
    if not token:
        return Response({"error": "Refresh token required"}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Verify JWT signature and structure
    try:
        payload = verify_token(token)
        if payload.get("type") != "refresh":
            return Response({"error": "Invalid token type"}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({"error": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED)

    # DB Verification (Check blacklist/revocation)
    try:
        refresh_token_obj = RefreshToken.objects.get(token=token)
        if refresh_token_obj.is_revoked:
            return Response({"error": "Token revoked"}, status=status.HTTP_401_UNAUTHORIZED)
    except RefreshToken.DoesNotExist:
        # Token valid JWT but not in DB? Possible if DB was wiped or token predates system.
        return Response({"error": "Token not found"}, status=status.HTTP_401_UNAUTHORIZED)

    # Rotation: Revoke old token
    refresh_token_obj.is_revoked = True
    refresh_token_obj.save()

    # Generate new tokens
    user = refresh_token_obj.user
    new_access_token = generate_access_token(user.id)
    new_refresh_token, new_refresh_exp = generate_refresh_token(user.id)
    
    # Persist new token
    RefreshToken.objects.create(
        user=user,
        token=new_refresh_token,
        expires_at=new_refresh_exp
    )

    response = Response({"access_token": new_access_token}, status=status.HTTP_200_OK)
    _set_refresh_cookie(response, new_refresh_token)
    return response


@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([ScopedRateThrottle])
def verify_token_view(request):
    request.throttle_scope = "auth"
    serializer = TokenVerifySerializer(data=request.data)
    if serializer.is_valid():
        token = serializer.validated_data["token"]
        try:
            payload = verify_token(token)
            return Response({"valid": True, "payload": payload}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"valid": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
