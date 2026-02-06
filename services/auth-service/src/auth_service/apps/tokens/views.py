from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import RefreshToken
from .serializers import TokenRefreshSerializer, TokenVerifySerializer
from ..utils.jwt_handler import generate_access_token, verify_token

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    serializer = TokenRefreshSerializer(data=request.data)
    if serializer.is_valid():
        refresh_token_str = serializer.validated_data['refresh_token']
        try:
            payload = verify_token(refresh_token_str)
            if payload.get('type') != 'refresh':
                return Response(
                    {'error': 'Invalid token type'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user_id = payload.get('user_id')
            user = User.objects.get(id=user_id)
            new_access_token = generate_access_token(user.id)
            return Response(
                {'access_token': new_access_token},
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_token_view(request):
    serializer = TokenVerifySerializer(data=request.data)
    if serializer.is_valid():
        token = serializer.validated_data['token']
        try:
            payload = verify_token(token)
            return Response(
                {'valid': True, 'payload': payload},
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response(
                {'valid': False, 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
