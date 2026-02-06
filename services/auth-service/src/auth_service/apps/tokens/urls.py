from django.urls import path
from .views import refresh_token, verify_token_view

urlpatterns = [
    path('refresh/', refresh_token, name='refresh-token'),
    path('verify/', verify_token_view, name='verify-token'),
]
