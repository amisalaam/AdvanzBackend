from channels.generic.websocket import AsyncWebsocketConsumer
import json


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        doctor_id = self.scope['url_route']['kwargs']['doctor_id']
        self.group_name = f'doctor_{doctor_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        message = json.loads(text_data)
        print("Received message:", message)

    async def slot_booked(self, event):
        message = event['message']

        await self.send(json.dumps({
            'type': 'slot_booked',
            'message': message,
        }))


class SuperuserNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'superuser_group'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        message = json.loads(text_data)
        print("admin_Received message:", message)

    async def slot_booked(self, event):
        message = event['message']
        await self.send(json.dumps({
            'type': 'notification',
            'message': message,
        }))

