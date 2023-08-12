import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from doctor import routing
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "advanzBackend.settings")

# Get the default Django application for ASGI
django_asgi_application = get_asgi_application()

# Get the Channels layer
channel_layer = get_channel_layer()

# Custom middleware to check Redis on every request
class RedisCheckMiddleware:
    def __init__(self, inner, channel_layer):
        self.inner = inner
        self.channel_layer = channel_layer

    async def check_redis(self):
        try:
            await self.channel_layer.send("test_channel", {"type": "ping"})
            print("Redis is working.aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        except Exception as e:
            print("Redis is not responding:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", str(e))

    async def __call__(self, scope, receive, send):
        # Perform the Redis check
        await self.check_redis()

        return await self.inner(scope, receive, send)

# Define the application routing
application = ProtocolTypeRouter(
    {
        "http": RedisCheckMiddleware(django_asgi_application, channel_layer),
        "websocket": AllowedHostsOriginValidator(AuthMiddlewareStack(
            URLRouter(routing.websocket_urlpatterns))
        ),
    }
)
