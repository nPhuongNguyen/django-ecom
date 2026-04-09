from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = "global"  # phòng chung

        # join group
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):
        # rời group
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        message = data.get("message")

        # gửi tới tất cả client trong group
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "chat_message",
                "message": message
            }
        )

    async def chat_message(self, event):
        # nhận từ Redis rồi gửi về client
        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))