from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User
from ..utils.validators import validate_email


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'password_confirm')

    def validate_email(self, value):
        validate_email(value)
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('User with this email already exists')
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
