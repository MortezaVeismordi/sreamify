from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from .jwt_handler import verify_token


def jwt_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        try:
            payload = verify_token(token)
            request.user_id = payload.get('user_id')
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return view_func(request, *args, **kwargs)
    return wrapper
