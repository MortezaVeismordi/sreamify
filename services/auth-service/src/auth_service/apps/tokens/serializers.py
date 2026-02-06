from rest_framework import serializers
from .models import RefreshToken


class RefreshTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefreshToken
        fields = ('id', 'user', 'token', 'created_at', 'expires_at', 'is_revoked')
        read_only_fields = ('id', 'created_at', 'expires_at')


class TokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class TokenVerifySerializer(serializers.Serializer):
    token = serializers.CharField()
