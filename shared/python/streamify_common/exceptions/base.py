from rest_framework.exceptions import APIException


class StreamifyException(APIException):
    """Base exception for Streamify services."""
    status_code = 500
    default_detail = 'An error occurred'
    default_code = 'error'


class ValidationError(StreamifyException):
    """Validation error exception."""
    status_code = 400
    default_detail = 'Validation error'
    default_code = 'validation_error'


class NotFoundError(StreamifyException):
    """Not found error exception."""
    status_code = 404
    default_detail = 'Resource not found'
    default_code = 'not_found'


class UnauthorizedError(StreamifyException):
    """Unauthorized error exception."""
    status_code = 401
    default_detail = 'Unauthorized'
    default_code = 'unauthorized'
