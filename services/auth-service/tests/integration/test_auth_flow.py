import pytest
from rest_framework import status


@pytest.mark.django_db
def test_registration_flow(api_client):
    response = api_client.post('/api/users/register/', {
        'email': 'newuser@example.com',
        'username': 'newuser',
        'first_name': 'New',
        'last_name': 'User',
        'password': 'Test1234',
        'password_confirm': 'Test1234',
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert 'access_token' in response.data
    assert 'refresh_token' in response.data


@pytest.mark.django_db
def test_login_flow(api_client, user):
    response = api_client.post('/api/users/login/', {
        'email': 'test@example.com',
        'password': 'Test1234',
    })
    assert response.status_code == status.HTTP_200_OK
    assert 'access_token' in response.data
