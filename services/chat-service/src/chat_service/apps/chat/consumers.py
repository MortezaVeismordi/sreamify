import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, Message

# Close code when middleware rejects (unauthorized)
WS_CLOSE_UNAUTHORIZED = 4001


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # User is set by JWTAuthMiddleware; if missing, middleware already closed the connection
        user = self.scope.get("user")
        if not user:
            await self.close(code=WS_CLOSE_UNAUTHORIZED)
            return

        self.user_id = user["id"]
        self.username = user.get("username") or user.get("email") or "unknown"
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"

        # Optional: restrict rooms by is_streamer etc.
        # if not user.get("is_streamer") and self.room_id == "streamer-only":
        #     await self.close(code=4403)
        #     return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        # Sender comes from scope['user'], not from client (so client cannot spoof)
        user_id = self.user_id
        username = self.username

        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get("message", "").strip()
        except (json.JSONDecodeError, TypeError):
            await self.send(text_data=json.dumps({"error": "Invalid JSON or missing 'message'"}))
            return

        if not message:
            return

        # Save message to database
        try:
            room = await ChatRoom.objects.aget(stream_id=self.room_id)
            await Message.objects.acreate(
                room=room, user_id=user_id, username=username, content=message
            )
        except ChatRoom.DoesNotExist:
            pass

        # Broadcast to room (include sender info from scope user)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user_id": user_id,
                "username": username,
            },
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "user_id": event["user_id"],
                    "username": event["username"],
                }
            )
        )
