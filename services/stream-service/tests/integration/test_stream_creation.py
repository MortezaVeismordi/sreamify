import pytest
from rest_framework import status


@pytest.mark.django_db
def test_create_stream_api(api_client):
    response = api_client.post(
        "/api/streams/",
        {
            "title": "Test Stream",
            "description": "Test Description",
            "user_id": 1,
            "status": "draft",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == "Test Stream"
