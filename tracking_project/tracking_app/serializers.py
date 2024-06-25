from rest_framework import serializers
from .models import *


class AdminUserTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUsersTable
        fields = ["target_name", "destination_point", "status"]

class TargetUsersTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetUsersTable
        fields = ["target_user", "target_pos", "target_pho"]
    

class LocationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationUpdate
        fields = "__all__"

class DestinationPointTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestinationPointTable
        fields = ["location_name", "address"]