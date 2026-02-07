from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from auth_service.utils.jwt_handler import generate_refresh_token
from auth_service.apps.tokens.models import RefreshToken


User = get_user_model()


class TokenTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com", username="testuser", password="Test1234"
        )

    def test_refresh_token_rotation(self):
        """Test that refreshing returns a new token and revokes the old one"""
        old_token, exp = generate_refresh_token(self.user.id)
        RefreshToken.objects.create(user=self.user, token=old_token, expires_at=exp)
        
        self.client.cookies["refresh_token"] = old_token
        response = self.client.post("/api/tokens/refresh/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_token = response.cookies["refresh_token"].value
        
        # Verify old token is now revoked
        self.assertTrue(RefreshToken.objects.get(token=old_token).is_revoked)
        # Verify new token exists and is not revoked
        self.assertTrue(RefreshToken.objects.filter(token=new_token, is_revoked=False).exists())
        self.assertNotEqual(old_token, new_token)

    def test_revoked_token_fails(self):
        """Test that using a revoked token returns 401"""
        token, exp = generate_refresh_token(self.user.id)
        RefreshToken.objects.create(user=self.user, token=token, expires_at=exp, is_revoked=True)
        
        self.client.cookies["refresh_token"] = token
        response = self.client.post("/api/tokens/refresh/")
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"], "Token revoked")

    def test_verify_token(self):
        refresh_token_str, _ = generate_refresh_token(self.user.id)
        response = self.client.post(
            "/api/tokens/verify/",
            {
                "token": refresh_token_str,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["valid"])
