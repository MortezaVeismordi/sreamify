from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Stream


class StreamTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.stream_data = {
            'title': 'Test Stream',
            'description': 'Test Description',
            'user_id': 1,
            'status': 'draft',
        }

    def test_create_stream(self):
        response = self.client.post('/api/streams/', self.stream_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Stream.objects.count(), 1)
