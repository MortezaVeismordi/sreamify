from django.core.mail import send_mail
from django.conf import settings


def send_email(to_email: str, subject: str, message: str):
    """Send email notification."""
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=False,
    )
