from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include


def health_view(request):
    return JsonResponse({"status": "ok", "service": "chat-service"})


urlpatterns = [
    path("health/", health_view),
    path("admin/", admin.site.urls),
    path("api/chat/", include("apps.chat.urls")),
]
