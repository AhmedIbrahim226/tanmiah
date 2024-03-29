"""
ASGI config for aatanmiah project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from django.urls import path

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from posts.channels.consumers import PostConsumer
from forums.channels.consumers import ForumFollowingNotification

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aatanmiah.settings')

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter([
                path('ws/post/consumer/', PostConsumer.as_asgi()),
                path('ws/forum/consumer/', ForumFollowingNotification.as_asgi()),
            ]))
        )
    }
)
