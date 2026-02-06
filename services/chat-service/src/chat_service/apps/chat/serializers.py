from rest_framework import serializers
from .models import ChatRoom, Message


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ('id', 'stream_id', 'name', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'room', 'user_id', 'username', 'content', 'created_at')
        read_only_fields = ('id', 'created_at')
