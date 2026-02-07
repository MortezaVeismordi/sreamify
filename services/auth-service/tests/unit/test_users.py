import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_user_creation(user):
    assert user.email == "test@example.com"
    assert user.check_password("Test1234")


@pytest.mark.django_db
def test_user_str(user):
    assert str(user) == "test@example.com"
