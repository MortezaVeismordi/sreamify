from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserRegistrationSerializer, UserSerializer, LoginSerializer
from auth_service.utils.jwt_handler import generate_access_token, generate_refresh_token


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def _set_refresh_cookie(self, response, token):
        """Helper to set secure refresh token cookie"""
        cookie_max_age = getattr(settings, "JWT_REFRESH_TOKEN_LIFETIME", 86400)
        response.set_cookie(
            key="refresh_token",
            value=token,
            max_age=cookie_max_age,
            httponly=True,
            secure=not settings.DEBUG,  # True in production
            samesite="Lax",
        )

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            access_token = generate_access_token(user.id)
            refresh_token = generate_refresh_token(user.id)

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
                refresh_token = generate_refresh_token(user.id)

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

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """Logout by clearing the refresh cookie"""
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
