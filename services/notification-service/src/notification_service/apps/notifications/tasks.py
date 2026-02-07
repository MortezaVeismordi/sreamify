from celery import shared_task
from .models import Notification
from ..utils.email import send_email
from ..utils.push import send_push_notification as send_push


@shared_task
def send_email_notification(notification_id):
    notification = Notification.objects.get(id=notification_id)
    send_email(
        to_email=f"user_{notification.user_id}@example.com",  # In production, get from user service
        subject=notification.title,
        message=notification.message,
    )


@shared_task
def send_push_notification(notification_id):
    notification = Notification.objects.get(id=notification_id)
    send_push(user_id=notification.user_id, title=notification.title, message=notification.message)
