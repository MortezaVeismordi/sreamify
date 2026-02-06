from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StreamViewSet, StreamViewViewSet

router = DefaultRouter()
router.register(r'streams', StreamViewSet, basename='stream')
router.register(r'views', StreamViewViewSet, basename='stream-view')

urlpatterns = [
    path('', include(router.urls)),
]
