import pytest
from rest_framework import status


@pytest.mark.django_db
@pytest.mark.e2e
def test_full_auth_flow(api_client):
    # Register
    register_response = api_client.post('/api/users/register/', {
        'email': 'e2e@example.com',
        'username': 'e2euser',
        'first_name': 'E2E',
        'last_name': 'Test',
        'password': 'Test1234',
        'password_confirm': 'Test1234',
    })
    assert register_response.status_code == status.HTTP_201_CREATED
    
    access_token = register_response.data['access_token']
    
    # Get user profile
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    profile_response = api_client.get('/api/users/me/')
    assert profile_response.status_code == status.HTTP_200_OK
    assert profile_response.data['email'] == 'e2e@example.com'
