from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Notification


class NotificationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_notification(self):
        response = self.client.post(
            "/api/notifications/",
            {
                "user_id": 1,
                "notification_type": "email",
                "title": "Test Notification",
                "message": "Test message",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Notification.objects.count(), 1)
