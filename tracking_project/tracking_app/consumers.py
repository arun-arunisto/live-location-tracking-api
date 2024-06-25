import json
import requests
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import LocationUpdate, TargetUsersTable, AdminUsersTable, DestinationPointTable



class TrackingTargetConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.target_name = self.scope["url_route"]["kwargs"]["target_name"]
        self.group_name = f"tracking_{self.target_name}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        latitude = text_data_json["latitude"]
        longitude = text_data_json["longitude"]
        target_name = text_data_json["target_name"]
        track_status = text_data_json["track_status"]

        try:
            target_data = await database_sync_to_async(TargetUsersTable.objects.get)(id=target_name)
            if target_data.current_location == None:
                url = "https://nominatim.openstreetmap.org/reverse"
                params = {
                    "lat":latitude,
                    "lon":longitude,
                    "format":"json",
                    "zoom":18,
                }
                headers = {
                    "User-Agent": "TrackingApp/1.0"
                }

                try:
                    response = requests.get(url, params=params, headers=headers)
                    response.raise_for_status()
                    data = response.json()
                    if data:
                        staring_point_name = str(latitude) +"," +str(longitude)
                        target_data.current_location = staring_point_name
                        if len(data["display_name"]) != 0:
                            staring_point_name = data["display_name"]
                            target_data.current_location = data["display_name"]
                        await database_sync_to_async(target_data.save)()
                        try:
                            admin_data = await database_sync_to_async(AdminUsersTable.objects.get)(target_name=target_data)
                            #print("admin_data.starting_point",admin_data.starting_point)
                            if admin_data.starting_point == None and admin_data.status == 'Stopped':
                                admin_data.starting_point = staring_point_name
                                admin_data.status = "Started"
                                await database_sync_to_async(admin_data.save)()
                        except AdminUsersTable.DoesNotExist:
                            return "Something went wrong"
                except:
                    return "Something went wrong"
            #print(target_data.current_location, "latitude", latitude, "longitude", longitude)
        except TargetUsersTable.DoesNotExist:
            return "User not exist"

        #save location update
        # try:
        #     location_update = LocationUpdate(target_name=target_data, latitude=latitude, longitude=longitude)
        #     await database_sync_to_async(location_update.save)()
        # except Exception as e:
        #     print(e)
        try:
            admin_data_latest = await database_sync_to_async(lambda: AdminUsersTable.objects.filter(target_name=target_data).latest('created_at'))()
        except AdminUsersTable.DoesNotExist:
            return "Query failed"
        try:
            location_update_old = await database_sync_to_async(lambda: LocationUpdate.objects.filter(admin_user_table_id=admin_data_latest, destination_point_id=admin_data_latest.destination_point, target_name=target_data).latest("timestamp"))()
            # if location_update_old.destination_point_id.latitude == latitude and location_update_old.destination_point_id.longitude == longitude:
            #     admin_data_latest.status = "Reached"
            #     try:
            #         location_update_new = LocationUpdate(admin_user_table_id=admin_data_latest, destination_point_id=admin_data_latest.destination_point, target_name=target_data, latitude=latitude, longitude=longitude)
            #         await database_sync_to_async(location_update_new.save)()
            #     except Exception as e:
            #         return "Error in location_update_new_query"
            print(location_update_old.latitude == latitude, location_update_old.longitude  == longitude, admin_data_latest.status)
            if location_update_old.latitude == latitude and location_update_old.longitude == longitude:
                admin_data_latest.status = "Stopped"
            else:
                admin_data_latest.status = "Traveling"
                try:
                    location_update_new = LocationUpdate(admin_user_table_id=admin_data_latest, destination_point_id=admin_data_latest.destination_point, target_name=target_data, latitude=latitude, longitude=longitude)
                    await database_sync_to_async(location_update_new.save)()
                except Exception as e:
                    return "Error in location_update_new_query"
            #print(admin_data_latest.status)
            await database_sync_to_async(admin_data_latest.save)()
            #print(location_update.target_name, "latitude", latitude, "longitude", longitude)
        except LocationUpdate.DoesNotExist:
            try:
                location_update_create = LocationUpdate(admin_user_table_id=admin_data_latest, destination_point_id=admin_data_latest.destination_point, target_name=target_data, latitude=latitude, longitude=longitude)
                await database_sync_to_async(location_update_create.save)()
            except Exception as e:
                pass

        #process incoming data (eg: location updated) and broadcast to the group
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type":"location_tracking",
                "latitude": latitude,
                "longitude": longitude,
                "target_name": target_name,
                "track_status":track_status
            }
        )
    
    async def location_tracking(self, event):
        latitude = event["latitude"]
        longitude = event["longitude"]
        target_name = event["target_name"]
        track_status = event["track_status"]
        await self.send(text_data=json.dumps({
            "latitude": latitude,
            "longitude": longitude,
            "target_name": target_name,
            "track_status":track_status
        }))


class TrackingTargetAdmin(AsyncWebsocketConsumer):
    # async def connect(self):
    #     self.admin_option_id = self.scope['url_route']['kwargs']['admin_option_id']
    #     self.group_name = f"admin_{self.admin_option_id}"
    #     await self.channel_layer.group_add(self.group_name, self.channel_name)
    #     await self.accept()
    #     print(f"WebSocket connected: {self.admin_option_id}")

    # async def disconnect(self, close_code):
    #     await self.channel_layer.group_discard(self.group_name, self.channel_name)
    #     print(f"WebSocket disconnected: {self.admin_option_id}")

    # async def receive(self, text_data):
    #     try:
    #         text_data_json = json.loads(text_data)
    #         target_user_id = text_data_json["target_user_id"]
    #         destination_point_id = text_data_json["destination_point_id"]

    #         target_user_data = await self.get_target_user(target_user_id)
    #         destination_data = await self.get_destination_point(destination_point_id)
    #         admin_option_data = await self.get_admin_option(self.admin_option_id)
    #         live_location_tracking = await self.get_latest_location_update(admin_option_data, destination_data, target_user_data)

    #         response_data = await self.response_data_for_admin(target_user_id, destination_point_id, live_location_tracking.latitude, live_location_tracking.tracking.longitude, live_location_tracking.admin_user__table_id.status)
    #         print("Data:", response_data)

    #         await self.send(text_data=json.dumps(response_data))

    #         await self.channel_layer.group_send(
    #             self.group_name,
    #             {
    #                 "type": "update_location",
    #                 "target_user_id": target_user_id,
    #                 "destination_point_id": destination_point_id,
    #             }
    #         )

    #     except json.JSONDecodeError:
    #         print("Invalid JSON format received")
    #     except KeyError as e:
    #         print(f"KeyError: Missing key {e}")
    #     except Exception as e:
    #         print(f"Error in receive: {e}")

    # @database_sync_to_async
    # def get_target_user(self, target_user_id):
    #     return TargetUsersTable.objects.get(id=target_user_id)

    # @database_sync_to_async
    # def get_destination_point(self, destination_point_id):
    #     return DestinationPointTable.objects.get(id=destination_point_id)

    # @database_sync_to_async
    # def get_admin_option(self, admin_option_id):
    #     return AdminUsersTable.objects.get(id=admin_option_id)

    # @database_sync_to_async
    # def get_latest_location_update(self, admin_option_data, destination_data, target_user_data):
    #     return LocationUpdate.objects.filter(
    #         admin_user_table_id=admin_option_data,
    #         destination_point_id=destination_data,
    #         target_name=target_user_data
    #     ).latest("timestamp")

    # async def update_location(self, event):
    #     target_user_id = event['target_user_id']
    #     destination_point_id = event['destination_point_id']
    #     await self.send(text_data=json.dumps({
    #         "target_user_id": target_user_id,
    #         "destination_point_id": destination_point_id,
    #     }))
    
    # async def response_data_for_admin(self, target_user_id, destination_point_id, latitude, longitude, status):
    #     response_data = {
    #         "target_user_id": target_user_id,
    #         "destination_point_id": destination_point_id,
    #         "latitude": latitude,
    #         "longitude": longitude,
    #         "status": status
    #     }

    #     return response_data
    
    # async def connect(self):
    #     self.admin_option_id = self.scope['url_route']['kwargs']['admin_option_id']
    #     self.target_user_id = self.scope["url_route"]["kwargs"]["target_user_id"]
    #     self.destination_point_id = self.scope["url_route"]["kwargs"]["destination_point_id"]
    #     await self.accept()
    #     print(self.admin_option_id, self.target_user_id, self.destination_point_id)
    #     print("Admin websocket connected")
    
    # async def disconnect(self, close_code):
    #     print("Admin websocket disconnected")

    # async def receive(self, text_data):
    #     try:
    #         target_user_data = await database_sync_to_async(TargetUsersTable.objects.get)(id=self.target_user_id)
    #         destination_data = await database_sync_to_async(DestinationPointTable.objects.get)(id=self.destination_point_id)
    #         admin_option_data = await database_sync_to_async(AdminUsersTable.objects.get)(id=self.admin_option_id)
    #         live_location_tracking = await database_sync_to_async(lambda: LocationUpdate.objects.filter(admin_user_table_id=admin_option_data, destination_point_id=destination_data, target_name=target_user_data).latest("timestamp"))()
    #     except Exception as e:
    #         print(e)
    #         return None

        
    #     await self.send(text_data=json.dumps({}))
    async def connect(self):
        self.admin_option_id = self.scope['url_route']['kwargs']['admin_option_id']
        self.group_name = f"admin_{self.admin_option_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        target_user_id = text_data_json["target_user_id"]
        destination_point_id = text_data_json["destination_point_id"]

        try:
            target_user_data = await database_sync_to_async(TargetUsersTable.objects.get)(id=target_user_id)
            destination_data = await database_sync_to_async(DestinationPointTable.objects.get)(id=destination_point_id)
            admin_option_data = await database_sync_to_async(AdminUsersTable.objects.get)(id=self.admin_option_id)
            live_location_tracking = await database_sync_to_async(
                    lambda: LocationUpdate.objects.filter(
                        admin_user_table_id = admin_option_data, 
                        destination_point_id = destination_data, 
                        target_name = target_user_data
                    ).latest("timestamp")
                )()
            
        except TargetUsersTable.DoesNotExist:
            print("Target user does not exist")
        
        except DestinationPointTable.DoesNotExist:
            print("Destination table does not exist")
        
        except AdminUsersTable.DoesNotExist:
            print("Admin table does not exist")
        
        except LocationUpdate.DoesNotExist:
            print("Location does not exist")
        
        except Exception as e:
            print("Error in data fetching", e)
        
        await self.send(text_data=json.dumps({
            "target_user_id":target_user_id,
            "destination_point_id":destination_point_id,
            "latitude":live_location_tracking.latitude,
            "longitude":live_location_tracking.longitude,
            "status":admin_option_data.status
        }))

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type":"update_location",
                "target_user_id":target_user_id,
                "destination_point_id":destination_point_id,
            }
        )

    async def update_location(self, event):
        target_user_id = event['target_user_id']
        destination_point_id = event['destination_point_id']
        await self.send(text_data=json.dumps({
            "target_user_id":target_user_id,
            "destination_point_id":destination_point_id,
        }))


