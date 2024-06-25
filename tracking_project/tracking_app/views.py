from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.shortcuts import render



# Create your views here.
class AdminOptionsListCreateView(generics.ListCreateAPIView):
    queryset = AdminUsersTable.objects.all()
    serializer_class = AdminUserTableSerializer


class AdminOptionsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdminUsersTable.objects.all().order_by("-id")
    serializer_class = AdminUserTableSerializer

class TargetUsersCreateView(generics.ListCreateAPIView):
    queryset = TargetUsersTable.objects.all()
    serializer_class = TargetUsersTableSerializer

class TargetUsersDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TargetUsersTable.objects.all().order_by("-id")
    serializer_class = TargetUsersTableSerializer

class LocationUpdateCreateView(generics.ListCreateAPIView):
    queryset = LocationUpdate.objects.all()
    serializer_class = LocationUpdateSerializer

class LocationUpdateListView(generics.ListAPIView):
    queryset = LocationUpdate.objects.all().order_by("-id")
    serializer_class = LocationUpdateSerializer

class LocationUpdateRetrieveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LocationUpdate.objects.all()
    serializer_class = LocationUpdateSerializer

class DestinationListCreateView(generics.ListCreateAPIView):
    queryset = DestinationPointTable.objects.all()
    serializer_class = DestinationPointTableSerializer

class DestinationPointDetailUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DestinationPointTable.objects.all()
    serializer_class = DestinationPointTableSerializer

#tracking_page
def tracking_page(request, pk):
    data = TargetUsersTable.objects.get(id=pk)
    print(data.target_user)
    return render(request, "tracking_page_new.html", {"target_name":data.id})

#map_view
def map_view(request, pk):
    data = AdminUsersTable.objects.filter(target_name=TargetUsersTable.objects.get(id=pk)).latest('created_at')
    return render(request, "map_view.html", {"target_name":data.id, "destination_point":[data.destination_point.latitude, data.destination_point.longitude], "status":data.status})


def map_view_admin(request, admin_option_id, target_user_id, destination_point_id):
    print(admin_option_id, target_user_id, destination_point_id)
    try:
        admin_data = AdminUsersTable.objects.get(id=admin_option_id)
        location_details = LocationUpdate.objects.filter(
            admin_user_table_id=admin_data,
            destination_point_id=admin_data.destination_point,
            target_name=admin_data.target_name 
        ).order_by("timestamp").first()
        if location_details == None:
            return render(request, "map_view_admin.html", {"status":"No data found"})
        starting_latitude = location_details.latitude
        starting_longitude = location_details.longitude
        print(starting_latitude, starting_longitude)
        destination_latitude = location_details.destination_point_id.latitude
        destination_longitude = location_details.destination_point_id.longitude
        track_status = location_details.admin_user_table_id.status
        print(destination_latitude, destination_longitude, track_status)
    except AdminUsersTable.DoesNotExist:
        print("Admin table does not exist")
        return "Admin table does not exist"
    except LocationUpdate.DoesNotExist:
        print("Location does not exist")
        return  "Location does not exist"
    except Exception as e:
        print(e)
        return e
    print("lat and lon:",starting_latitude, starting_longitude)
    return render(request, 'map_view_admin.html', {"admin_option_id":admin_option_id, 
                                                   "target_user_id":target_user_id, 
                                                   "destination_point_id":destination_point_id,
                                                   "starting_latitdue":starting_latitude,
                                                   "starting_longitude":starting_longitude,
                                                   "destination_latitude":destination_latitude,
                                                   "destination_longitude":destination_longitude,
                                                   "track_status":track_status})



