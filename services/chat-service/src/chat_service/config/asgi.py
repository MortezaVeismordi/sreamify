import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from chat_service.middleware import JWTAuthMiddleware
from apps.chat import routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat_service.config.settings.prod")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": JWTAuthMiddleware(URLRouter(routing.websocket_urlpatterns)),
    }
)
