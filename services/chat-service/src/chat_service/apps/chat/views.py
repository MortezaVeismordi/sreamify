from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer


class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [AllowAny]
    lookup_field = 'stream_id'

    @action(detail=True, methods=['get'])
    def messages(self, request, stream_id=None):
        room = self.get_object()
        messages = room.messages.all()[:100]  # Last 100 messages
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Message.objects.all()
        room_id = self.request.query_params.get('room', None)
        if room_id:
            queryset = queryset.filter(room_id=room_id)
        return queryset
