from django.db import models

# Create your models here.

#destination point table
class DestinationTable(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    address = models.CharField(max_length=100, null=False, blank=False)
    latitude = models.CharField(max_length=100, null=False, blank=False)
    longitude = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Location: {self.name}"

class EmployeeTable(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    position = models.CharField(max_length=100, null=False, blank=False)
    mail_id = models.EmailField(max_length=100, null=False, blank=False, unique=True)


    def __str__(self):
        return f"Employee: {self.name}"

class TaskTable(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    description = models.TextField(null=True)
    starting_point = models.CharField(max_length=255, null=True, blank=True)
    destination = models.ForeignKey(DestinationTable, on_delete=models.SET_NULL, null=True)
    assigned_employee = models.ForeignKey(EmployeeTable, on_delete=models.SET_NULL, null=True)
    travel_status = models.CharField(max_length=50, choices=[
        ('Stopped', 'Stopped'),
        ('Traveling', 'Traveling'),
        ('Reached', 'Reached'),
    ])
    status = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
    ])

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Task {self.name}"

class LocationTrackingTable(models.Model):
    task_id = models.ForeignKey(TaskTable, on_delete=models.CASCADE)
    destination_id = models.ForeignKey(DestinationTable, on_delete=models.SET_NULL, null=True)
    employee_id = models.ForeignKey(EmployeeTable, on_delete=models.SET_NULL, null=True)
    latitude = models.CharField(max_length=100, null=False, blank=False)
    longitude = models.CharField(max_length=100, null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    







