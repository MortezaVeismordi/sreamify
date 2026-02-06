import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        email='test@example.com',
        username='testuser',
        password='Test1234',
        first_name='Test',
        last_name='User',
    )


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()
