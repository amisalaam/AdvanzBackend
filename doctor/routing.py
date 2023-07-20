from django.urls import re_path
from .consumers import NotificationConsumer,SuperuserNotificationConsumer


websocket_urlpatterns = [
    re_path(r'ws/doctor/(?P<doctor_id>\d+)/$', NotificationConsumer.as_asgi()),
    re_path(r'ws/superuser-notifications/$', SuperuserNotificationConsumer.as_asgi()),
]
