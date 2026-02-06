from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include

def health_view(request):
    return JsonResponse({"status": "ok", "service": "notification-service"})

urlpatterns = [
    path('health/', health_view),
    path('admin/', admin.site.urls),
    path('api/', include('apps.notifications.urls')),
]
