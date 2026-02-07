import pytest
from apps.streams.models import Stream


@pytest.mark.django_db
def test_stream_creation():
    stream = Stream.objects.create(
        title="Test Stream", description="Test Description", user_id=1, status="draft"
    )
    assert stream.title == "Test Stream"
    assert stream.status == "draft"
