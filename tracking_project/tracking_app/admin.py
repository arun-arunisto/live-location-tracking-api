from django.contrib import admin
from .models import *
from django.contrib.admin.models import LogEntry


class AdminUserDashBoard(admin.ModelAdmin):
    list_display = ["id", "target_name", "starting_point", "destination_point", "status", "created_at"]
    list_filter = ["target_name", "status"]

class TargetUserDashBoard(admin.ModelAdmin):
    list_display = ["id", "target_user", "target_pos", "target_pho", "current_location"]
    list_filter = ["target_user"]

class LocationUpdateDashBoard(admin.ModelAdmin):
    list_display = ["id", "target_name", "latitude", "longitude", "timestamp"]
    list_filter = ["target_name"]

class DestinationPointTableDashBoard(admin.ModelAdmin):
    list_display = ["id", "location_name", "latitude", "longitude"]

admin.site.register(AdminUsersTable, AdminUserDashBoard)
admin.site.register(TargetUsersTable, TargetUserDashBoard)
admin.site.register(LocationUpdate, LocationUpdateDashBoard)
admin.site.register(DestinationPointTable, DestinationPointTableDashBoard)
