from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import ChatRoom, Message


class ChatTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.room = ChatRoom.objects.create(
            stream_id=1,
            name='Test Room'
        )

    def test_create_message(self):
        response = self.client.post('/api/chat/messages/', {
            'room': self.room.id,
            'user_id': 1,
            'username': 'testuser',
            'content': 'Hello, world!',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)
