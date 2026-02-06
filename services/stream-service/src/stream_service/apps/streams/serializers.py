from rest_framework import serializers
from .models import Stream, StreamView


class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = (
            'id', 'title', 'description', 'user_id', 'category', 'thumbnail',
            'video_url', 'status', 'viewer_count', 'started_at', 'ended_at',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'viewer_count')


class StreamViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamView
        fields = ('id', 'stream', 'user_id', 'ip_address', 'viewed_at')
        read_only_fields = ('id', 'viewed_at')
