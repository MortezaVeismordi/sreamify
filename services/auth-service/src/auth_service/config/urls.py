from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include


def health_view(request):
    return JsonResponse({"status": "ok", "service": "auth-service"})


urlpatterns = [
    path("health/", health_view),
    path("admin/", admin.site.urls),
    path("api/users/", include("auth_service.apps.users.urls")),
    path("api/tokens/", include("auth_service.apps.tokens.urls")),
]
