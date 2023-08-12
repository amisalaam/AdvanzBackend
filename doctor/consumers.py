from channels.generic.websocket import AsyncWebsocketConsumer
import json


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            doctor_id = self.scope['url_route']['kwargs']['doctor_id']
            self.group_name = f'doctor_{doctor_id}'

            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )

            await self.accept()
        except Exception as e:
            print("Error in connect:", e)

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
        except Exception as e:
            print("Error in disconnect:", e)

    async def receive(self, text_data):
        try:
            message = json.loads(text_data)
            print("Received message:", message)
        except Exception as e:
            print("Error in receive:", e)

    async def slot_booked(self, event):
        try:
            message = event['message']

            await self.send(json.dumps({
                'type': 'slot_booked',
                'message': message,
            }))
        except Exception as e:
            print("Error in slot_booked:", e)


class SuperuserNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.group_name = 'superuser_group'
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            print('connected ')
            await self.accept()
        except Exception as e:
            print("Error in connect 77777777777777777777777777777777777777777777777:", e)

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
        except Exception as e:
            print("Error in disconnect: 66666666666666666666666666666666", e)

    async def receive(self, text_data):
        try:
            message = json.loads(text_data)
            print("admin_Received message:", message)
        except Exception as e:
            print("Error in receive:55555555555555555555555555", e)

    async def slot_booked(self, event):
        try:
            message = event['message']
            await self.send(json.dumps({
                'type': 'notification',
                'message': message,
            }))
        except Exception as e:
            print("Error in slot_booked:4444444444444444444444444444444444", e)
