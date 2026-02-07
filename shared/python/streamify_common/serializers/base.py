from rest_framework import serializers


class BaseSerializer(serializers.Serializer):
    """Base serializer with common functionality."""

    pass


class BaseModelSerializer(serializers.ModelSerializer):
    """Base model serializer with common fields."""

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        abstract = True
