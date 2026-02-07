import logging
from django.http import JsonResponse
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware:
    """Error handler middleware for Streamify services."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, APIException):
            return JsonResponse({"error": exception.detail}, status=exception.status_code)
        logger.exception("Unhandled exception")
        return JsonResponse({"error": "Internal server error"}, status=500)
