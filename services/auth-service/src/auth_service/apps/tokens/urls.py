from django.urls import path
from .views import refresh_token, verify_token_view, verify_bearer_view

urlpatterns = [
    path("refresh/", refresh_token, name="refresh-token"),
    path("verify/", verify_token_view, name="verify-token"),
    path("verify-bearer/", verify_bearer_view, name="verify-bearer"),
]
