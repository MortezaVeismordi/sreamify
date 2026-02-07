from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "password": "Test1234",
            "password_confirm": "Test1234",
        }

    def test_user_registration(self):
        # Remove password_confirm if serializer doesn't strictly require it in the dict (assuming it does)
        response = self.client.post("/api/users/register/", self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access_token", response.data)
        self.assertNotIn("refresh_token", response.data)
        self.assertIn("refresh_token", response.cookies)

    def test_user_login(self):
        # Remove password_confirm for create_user as it's not a model field
        data = self.user_data.copy()
        data.pop("password_confirm")
        User.objects.create_user(**data)
        
        response = self.client.post(
            "/api/users/login/",
            {
                "email": self.user_data["email"],
                "password": self.user_data["password"],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.cookies)

    def test_user_logout(self):
        data = self.user_data.copy()
        data.pop("password_confirm")
        user = User.objects.create_user(**data)
        
        # Manually set cookie to simulate logged in state
        self.client.cookies["refresh_token"] = "some_token"
        response = self.client.post("/api/users/logout/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if cookie is cleared (expiry set to past)
        self.assertEqual(response.cookies["refresh_token"].value, "")
