import pytest
from apps.notifications.models import Notification


@pytest.mark.django_db
def test_notification_creation():
    notification = Notification.objects.create(
        user_id=1, notification_type="email", title="Test", message="Test message"
    )
    assert notification.user_id == 1
    assert notification.is_read == False


@pytest.mark.django_db
def test_mark_as_read():
    notification = Notification.objects.create(
        user_id=1, notification_type="email", title="Test", message="Test message"
    )
    notification.mark_as_read()
    assert notification.is_read == True
    assert notification.read_at is not None
