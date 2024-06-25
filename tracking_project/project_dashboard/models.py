from django.db import models

class AppDetails(models.Model):
    name = models.CharField(max_length=100)
    info = models.TextField()
    endpoints = models.TextField()
    connection = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"API : {self.name}"