from rest_framework.views import exception_handler
from .base import StreamifyException


def custom_exception_handler(exc, context):
    """Custom exception handler for Streamify services."""
    response = exception_handler(exc, context)

    if isinstance(exc, StreamifyException):
        custom_response_data = {
            'error': {
                'code': exc.default_code,
                'message': exc.default_detail,
            }
        }
        response.data = custom_response_data

    return response
