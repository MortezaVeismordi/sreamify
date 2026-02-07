from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from .models import User
from .serializers import (
    UserRegistrationSerializer, 
    UserSerializer, 
    LoginSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer
)
from auth_service.utils.jwt_handler import generate_access_token, generate_refresh_token
from auth_service.apps.tokens.models import RefreshToken


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    def _set_refresh_cookie(self, response, token):
        """Helper to set secure refresh token cookie"""
        cookie_max_age = getattr(settings, "JWT_REFRESH_TOKEN_LIFETIME", 86400)
        response.set_cookie(
            key="refresh_token",
            value=token,
            max_age=cookie_max_age,
            httponly=True,
            secure=not settings.DEBUG,  # True in production
            samesite="Strict",
        )

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            access_token = generate_access_token(user.id)
            refresh_token, refresh_exp = generate_refresh_token(user.id)
            
            # Persist token
            RefreshToken.objects.create(
                user=user,
                token=refresh_token,
                expires_at=refresh_exp
            )

            response = Response(
                {
                    "user": UserSerializer(user).data,
                    "access_token": access_token,
                    # Refresh token is now in cookie
                },
                status=status.HTTP_201_CREATED,
            )
            self._set_refresh_cookie(response, refresh_token)
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(request, username=email, password=password)
            
            if user:
                access_token = generate_access_token(user.id)
                refresh_token, refresh_exp = generate_refresh_token(user.id)

                # Persist token
                RefreshToken.objects.create(
                    user=user,
                    token=refresh_token,
                    expires_at=refresh_exp
                )

                response = Response(
                    {
                        "user": UserSerializer(user).data,
                        "access_token": access_token,
                    },
                    status=status.HTTP_200_OK,
                )
                self._set_refresh_cookie(response, refresh_token)
                return response
            
            # Check if authentication failed due to inactive account
            try:
                user_obj = User.objects.get(email=email)
                if user_obj.check_password(password) and not user_obj.is_active:
                     return Response({"error": "Account is inactive"}, status=status.HTTP_403_FORBIDDEN)
            except User.DoesNotExist:
                pass

            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def logout(self, request):
        """Logout by revoking the token and clearing the cookie"""
        token = request.COOKIES.get("refresh_token")
        if token:
            RefreshToken.objects.filter(token=token).update(is_revoked=True)
            
        response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        response.delete_cookie("refresh_token")
        return response

    @action(detail=False, methods=["get", "put"], permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.method == "GET":
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = UserSerializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def password_reset(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.filter(email=email).first()
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
                
                send_mail(
                    "Password Reset Request",
                    f"Click the link to reset your password: {reset_url}",
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
            return Response({"message": "If an account exists with this email, a reset link has been sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def password_reset_confirm(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            uidb64 = request.data.get("uid")
            token = request.data.get("token")
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            if user and default_token_generator.check_token(user, token):
                user.set_password(serializer.validated_data["new_password"])
                user.save()
                return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
