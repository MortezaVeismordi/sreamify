import pytest
from apps.notifications.tasks import send_email_notification, send_push_notification
from apps.notifications.models import Notification


@pytest.mark.django_db
def test_send_email_notification():
    notification = Notification.objects.create(
        user_id=1, notification_type="email", title="Test", message="Test message"
    )
    # In production, mock the email sending
    send_email_notification(notification.id)
    # Assert email was sent (would need mocking in production)
