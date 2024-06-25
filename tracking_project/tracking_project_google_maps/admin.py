from django.contrib import admin
from .models import DestinationTable, EmployeeTable, TaskTable, LocationTrackingTable

# Register your models here.
class DestinationDashBoard(admin.ModelAdmin):
    list_display = ["name", "address", "latitude", "longitude"]
    list_display_links = ["name"]

class EmployeeDashBoard(admin.ModelAdmin):
    list_display = ["name", "position", "mail_id"]
    list_display_links = ["name"]

class TaskDashBoard(admin.ModelAdmin):
    list_display = ["name", "description", "starting_point", "destination", "assigned_employee", "travel_status", "status"]
    list_display_links = ["name"]

class LocationTrackingDashBoard(admin.ModelAdmin):
    list_display = ["task_id", "destination_id", "employee_id", "latitude", "longitude", "timestamp"]
    list_display_links = ["task_id"]

admin.site.register(DestinationTable, DestinationDashBoard)
admin.site.register(EmployeeTable, EmployeeDashBoard)
admin.site.register(TaskTable, TaskDashBoard)
admin.site.register(LocationTrackingTable, LocationTrackingDashBoard)
