import pytest
from ..utils.jwt_handler import generate_access_token, generate_refresh_token, verify_token


@pytest.mark.django_db
def test_generate_access_token(user):
    token = generate_access_token(user.id)
    assert token is not None
    assert isinstance(token, str)


@pytest.mark.django_db
def test_verify_token(user):
    token = generate_access_token(user.id)
    payload = verify_token(token)
    assert payload["user_id"] == user.id
    assert payload["type"] == "access"
