from django.urls import path, re_path
from .consumers import TrackingTargetConsumer, TrackingTargetAdmin

websocket_urlpatterns = [
    re_path(r"ws/tracking/(?P<target_name>\w+)/$", TrackingTargetConsumer.as_asgi()),
    re_path(r"ws/admin/(?P<admin_option_id>\w+)/$", TrackingTargetAdmin.as_asgi())
]
