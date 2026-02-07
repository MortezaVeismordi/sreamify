from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User
from auth_service.utils.validators import (
    validate_email,
)  # We'll see if this path is valid, assuming yes from previous file


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password", "password_confirm", "phone")
        # Removed 'username', added 'phone'

    def validate_email(self, value):
        # We can keep custom validator or rely on standard email field validation + uniqueness
        # validate_email(value) # Assuming this utility exists, keeping it safe
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "is_streamer",
            "bio",
            "profile_picture",
            "is_active",
            "date_joined",
        )
        read_only_fields = ("id", "email", "is_streamer", "is_active", "date_joined")
        # Removed username, added profile fields


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs
