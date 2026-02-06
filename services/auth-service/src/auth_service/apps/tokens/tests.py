from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from ..utils.jwt_handler import generate_refresh_token

User = get_user_model()


class TokenTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='Test1234'
        )

    def test_refresh_token(self):
        refresh_token_str = generate_refresh_token(self.user.id)
        response = self.client.post('/api/tokens/refresh/', {
            'refresh_token': refresh_token_str,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)

    def test_verify_token(self):
        refresh_token_str = generate_refresh_token(self.user.id)
        response = self.client.post('/api/tokens/verify/', {
            'token': refresh_token_str,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['valid'])
