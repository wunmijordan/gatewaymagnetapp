import json
import logging
from datetime import datetime
from django.utils.timezone import now
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

logger = logging.getLogger(__name__)

def get_user_color(user_id):
    colors = [
        "bg-blue-lt text-white","bg-green-lt text-white","bg-orange-lt text-white",
        "bg-purple-lt text-white","bg-pink-lt text-white","bg-cyan-lt text-white",
        "bg-yellow-lt text-white","bg-red-lt text-white","bg-indigo-lt text-white",
        "bg-teal-lt text-white","bg-lime-lt text-white","bg-amber-lt text-white",
        "bg-fuchsia-lt text-white","bg-emerald-lt text-white","bg-violet-lt text-white",
        "bg-rose-lt text-white","bg-sky-lt text-white","bg-orange-200 text-white",
        "bg-purple-200 text-white","bg-pink-200 text-white"
    ]
    return colors[user_id % len(colors)]

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "group_chat"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            sender_id = data.get("sender_id")
            message = data.get("message", "").strip()
            guest_id = data.get("guest_id")
            parent_id = data.get("reply_to_id")

            # Ignore empty messages with no guest or reply
            if not message and not guest_id:
                return

            # Save message first (returns a dict now)
            saved_message = await self.create_message(sender_id, message, guest_id, parent_id)

            # Prepare payload for immediate delivery
            payload = {**saved_message, "type": "chat_message", "color": get_user_color(sender_id)}

            # Send to group
            await self.channel_layer.group_send(self.room_group_name, payload)

        except Exception as e:
            logger.error(f"WebSocket receive error: {e}")

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    # Helpers to get user info without blocking
    @sync_to_async(thread_sensitive=False)
    def get_sender_name(self, sender_id):
        from .models import CustomUser
        user = CustomUser.objects.only('full_name', 'username').get(id=sender_id)
        return user.full_name or user.username

    @sync_to_async(thread_sensitive=False)
    def get_sender_image(self, sender_id):
        from .models import CustomUser
        user = CustomUser.objects.only('image').get(id=sender_id)
        return user.image.url if user.image else None

    @staticmethod
    def now_iso():
        from datetime import datetime
        return now().isoformat()

    @sync_to_async
    def get_guest_info(self, guest_id):
        from guests.models import GuestEntry
        g = GuestEntry.objects.get(id=guest_id)
        return {
            "id": g.id,
            "name": g.full_name,
            "custom_id": g.custom_id,
            "image": g.picture.url if g.picture else None,
            "title": g.title,
            "date_of_visit": g.date_of_visit.strftime("%Y-%m-%d") if g.date_of_visit else "",
        }

    @sync_to_async
    def get_parent_info(self, parent_id):
        from .models import ChatMessage
        p = ChatMessage.objects.select_related("sender", "guest_card").get(id=parent_id)
        parent_data = {
            "id": p.id,
            "sender_name": p.sender.full_name or p.sender.username,
            "sender_title": p.sender.title,
            "message": p.message[:50],  # truncate preview
        }
        if p.guest_card:
            g = p.guest_card
            parent_data["guest"] = {
                "id": g.id,
                "name": g.full_name,
                "title": g.title,
                "image": g.picture.url if g.picture else None,
                "date_of_visit": g.date_of_visit.strftime("%Y-%m-%d") if g.date_of_visit else "",
            }
        return parent_data

    @sync_to_async(thread_sensitive=False)
    def create_message(self, sender_id, message, guest_id=None, parent_id=None):
        from .models import ChatMessage, CustomUser
        from guests.models import GuestEntry

        try:
            sender = CustomUser.objects.get(id=sender_id)
            guest_card = GuestEntry.objects.filter(id=guest_id).first() if guest_id else None
            parent = ChatMessage.objects.filter(id=parent_id).first() if parent_id else None

            saved = ChatMessage.objects.create(
                sender=sender,
                message=message,
                guest_card=guest_card,
                parent=parent
            )

            payload = {
                "id": saved.id,
                "message": saved.message,
                "created_at": saved.created_at.isoformat(),
                "sender_id": sender.id,
                "sender_title": sender.title,
                "sender_name": sender.full_name or sender.username,
                "sender_image": sender.image.url if sender.image else None,
                "guest": None,
                "parent": None,
                "reply_to_id": parent.id if parent else None,   # 👈 here
            }

            if guest_card:
                payload["guest"] = {
                    "id": guest_card.id,
                    "name": guest_card.full_name,
                    "custom_id": guest_card.custom_id,
                    "image": guest_card.picture.url if guest_card.picture else None,
                    "title": guest_card.title,
                    "date_of_visit": guest_card.date_of_visit.strftime("%Y-%m-%d") if guest_card.date_of_visit else "",
                }

            if parent:
                parent_data = {
                    "id": parent.id,
                    "sender_title": parent.sender.title,
                    "sender_name": parent.sender.full_name or parent.sender.username,
                    "message": parent.message[:50],
                }
                if parent.guest_card:
                    g = parent.guest_card
                    parent_data["guest"] = {
                        "id": g.id,
                        "name": g.full_name,
                        "title": g.title,
                        "image": g.picture.url if g.picture else None,
                        "date_of_visit": g.date_of_visit.strftime("%Y-%m-%d") if g.date_of_visit else "",
                    }
                payload["parent"] = parent_data

            return payload

        except Exception as e:
            logger.error(f"create_message failed: {e}")
            return {}   # 👈 return safe dict instead of None
