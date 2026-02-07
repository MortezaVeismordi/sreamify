from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


def health_view(request):
    return JsonResponse({"status": "ok", "service": "stream-service"})


urlpatterns = [
    path("health/", health_view),
    path("admin/", admin.site.urls),
    path("api/", include("apps.streams.urls")),
    path("api/", include("apps.categories.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
