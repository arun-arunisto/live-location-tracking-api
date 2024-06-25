from django.db import models
import requests
import json

# Create your models here.


class DestinationPointTable(models.Model):
    location_name = models.CharField(max_length=255)
    address = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Location - {self.location_name}"
    
    def save(self, *args, **kwargs):
        if not self.latitude or self.longitude:
            url = "https://nominatim.openstreetmap.org/search"

            params = {
                "q":self.address,
                "format":"json",
                "limit":1
            }

            headers = {
                "User-Agent": "TrackingApp/1.0"
            }

            try:
                response = requests.get(url, params=params, headers=headers)
                response.raise_for_status()
                data = response.json()
                if data:
                    self.latitude = data[0]["lat"]
                    self.longitude = data[0]["lon"]
            except Exception as e:
                print(e)
        
        return super().save(*args, **kwargs)

class TargetUsersTable(models.Model):
    target_user = models.CharField(max_length=255, unique=True)
    target_pos = models.CharField(max_length=255, null=True, blank=True)
    target_pho = models.CharField(max_length=255, null=True, blank=True)
    current_location = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"Target - {self.target_user}"

class AdminUsersTable(models.Model):
    target_name = models.ForeignKey(TargetUsersTable, on_delete=models.SET_NULL, null=True, blank=True)
    starting_point = models.CharField(max_length=255, null=True, blank=True)
    destination_point = models.ForeignKey(DestinationPointTable, on_delete=models.SET_NULL, null=True, blank=True)
    status  = models.CharField(max_length=50, choices=[
        ('Stopped', 'Stopped'),
        ('Traveling', 'Traveling'),        
        ('Started', 'Started'),
        ('Reached', 'Reached'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tracking_id: {self.id} for {self.target_name}"

class LocationUpdate(models.Model):
    admin_user_table_id = models.ForeignKey(AdminUsersTable, on_delete=models.CASCADE, null=True, blank=True)
    destination_point_id = models.ForeignKey(DestinationPointTable, on_delete=models.SET_NULL, null=True, blank=True)
    target_name = models.ForeignKey(TargetUsersTable, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"Location status id: {self.id} for {self.target_name}"



    
