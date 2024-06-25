from django.urls import path
from .views import *

urlpatterns = [
    path('admin_options_create_view/', AdminOptionsListCreateView.as_view(), name="admin-options-create"),
    path('admin_options_detail_view/<int:pk>/',AdminOptionsDetailView.as_view(), name='admin-options-detail'),
    path('target_users_create_view/', TargetUsersCreateView.as_view(), name="target-users-create"),
    path('target_users_detail_view/<int:pk>/', TargetUsersDetailView.as_view()),
    path('location_updates_create_view/', LocationUpdateCreateView.as_view(), name="location-updates-create"),
    path('location_updates_detail_view/<int:pk>/', LocationUpdateRetrieveUpdateView.as_view(), name="location-updates-detail"),
    path('location_update_list_view/', LocationUpdateListView.as_view(), name="location-update-list"),
    path('destination_list_create_view/', DestinationListCreateView.as_view(), name="destination-point-create"),
    path('destination_list_detail_view/<int:pk>/', DestinationPointDetailUpdateView.as_view(), name="destination-detail-view"),
    path('map_view/<int:pk>/', map_view, name="map-view"),
    path('tracking_page/<int:pk>/', tracking_page, name="tracking-page"),
    path('map_view_admin/<int:admin_option_id>/<int:target_user_id>/<int:destination_point_id>/', map_view_admin, name="map-view-admin"),
]