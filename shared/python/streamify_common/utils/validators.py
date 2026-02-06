import re
from django.core.exceptions import ValidationError


def validate_email(email: str):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError('Invalid email format')


def validate_phone(phone: str):
    """Validate phone number format."""
    pattern = r'^\+?1?\d{9,15}$'
    if not re.match(pattern, phone):
        raise ValidationError('Invalid phone number format')
