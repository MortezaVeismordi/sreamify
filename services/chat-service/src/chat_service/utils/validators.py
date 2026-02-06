from django.core.exceptions import ValidationError


def validate_message_content(content):
    if not content or len(content.strip()) == 0:
        raise ValidationError('Message content cannot be empty')
    if len(content) > 1000:
        raise ValidationError('Message content cannot exceed 1000 characters')
