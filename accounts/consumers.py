import json, re
import logging
from datetime import timedelta
from django.utils.timezone import now
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.files.storage import default_storage


logger = logging.getLogger(__name__)



# =================== Helpers ===================
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


# ---------- Helper ----------
def handle_file_upload(file_url):
    """
    Upload to Cloudinary in production, or use MEDIA_ROOT path in development.
    """
    from cloudinary.uploader import upload as cloudinary_upload
    if not file_url:
        return None

    # ✅ Keep local media in dev
    if settings.DEBUG:
        if file_url.startswith("http"):
            return file_url
        return file_url

    # ✅ Upload to Cloudinary in prod
    if file_url.startswith("http"):
        return file_url
    try:
        upload_result = cloudinary_upload(file_url, folder="chat/files/")
        return upload_result.get("secure_url")
    except Exception as e:
        logger.warning("Cloudinary upload failed: %s", e)
        return file_url


# =================== Chat Consumer ===================
class ChatConsumer(AsyncWebsocketConsumer):

    # ---------- WebSocket Lifecycle ----------
    async def connect(self):
        self.room_group_name = "group_chat"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # ✅ Send latest pinned previews on connect
        recent = await self.get_recent_pinned()
        await self.send(text_data=json.dumps({
            "type": "pinned_preview",
            "messages": recent
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            if data.get("action"):
                await self.handle_action(data)
            else:
                await self.handle_new_message(data)
        except Exception as e:
            logger.error(f"WebSocket receive error: {e}")

    # ---------- Action Handler ----------
    async def handle_action(self, data):
        action = data.get("action")
        sender_id = data.get("sender_id")

        if action == "pin":
            message_ids = data.get("message_ids", [])
            pinned_map = await self.handle_pin(message_ids, sender_id)

            # 🔹 Get sender info for pinned_by
            from .models import CustomUser
            try:
                pinner = await sync_to_async(CustomUser.objects.get)(id=sender_id)
                pinned_by_payload = {
                    "id": pinner.id,
                    "name": pinner.full_name or pinner.username,
                    "title": getattr(pinner, "title", "")
                }
            except Exception:
                pinned_by_payload = None

            # 🔹 1. Tell all clients to toggle bubble flags
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "message_pinned",
                    "message_ids": message_ids,
                    "pinned": pinned_map,
                    "pinned_by": pinned_by_payload,
                }
            )

            # 🔹 2. Broadcast updated pinned preview stack
            recent = await self.get_recent_pinned()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "pinned_preview",
                    "messages": recent
                }
            )
            return

        elif action == "reply":
            # client handles reply preview
            return

        else:
            logger.debug("Unknown action received: %s", action)

    # ---------- New Message Handler ----------
    async def handle_new_message(self, data):
        sender_id = data.get("sender_id")
        message = data.get("message", "").rstrip()
        guest_id = data.get("guest_id")
        parent_id = data.get("reply_to_id")
        mentions_ids = data.get("mentions", [])
        file_data = data.get("file") or {} # expect dict {url,name,size,type}
        file_url = file_data.get("url")
        link_preview = data.get("link_preview")

        if not message.strip() and not guest_id and not file_url and not link_preview:
            return

        saved_message = await self.create_message(sender_id, message, guest_id, parent_id, mentions_ids, file_url, link_preview)
        payload = {**saved_message, "type": "chat_message", "color": get_user_color(sender_id)}
        await self.channel_layer.group_send(self.room_group_name, payload)

    # ---------- WebSocket Group Events ----------
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def message_pinned(self, event):
        await self.send(text_data=json.dumps(event))

    async def pinned_preview(self, event):
        """Broadcast pinned preview list"""
        await self.send(text_data=json.dumps({
            "type": "pinned_preview",
            "messages": event["messages"]
        }))

    # =================== Database / Sync Handlers ===================
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
            "message": p.message[:50],
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

    # ---------- Action Handlers ----------
    @sync_to_async
    def handle_pin(self, message_ids, sender_id):
        from .models import ChatMessage
        res = {}
        for mid in message_ids:
            try:
                m = ChatMessage.objects.filter(id=mid).first()
                if not m:
                    continue

                # Toggle pinned state
                if m.pinned:
                    m.pinned = False
                    m.pinned_at = None
                    m.pinned_by = None
                else:
                    m.pinned = True
                    m.pinned_at = now()
                    m.pinned_by_id = sender_id
                m.save(update_fields=["pinned", "pinned_at", "pinned_by_id"])
                res[str(mid)] = m.pinned
            except Exception:
                logger.exception("Failed to toggle pin %s", mid)
        return res

    # ---------- Helpers ----------
    @sync_to_async
    def get_recent_pinned(self):
        from .models import ChatMessage
        from .utils import serialize_message, build_mention_helpers
        cutoff = now() - timedelta(days=14)

        # Auto-unpin expired ones
        ChatMessage.objects.filter(pinned=True, pinned_at__lt=cutoff).update(
            pinned=False, pinned_at=None, pinned_by=None
        )

        pinned = (
            ChatMessage.objects.filter(pinned=True, pinned_at__gte=cutoff)
            .select_related("pinned_by", "sender", "guest_card")
            .order_by("-pinned_at")[:3]
        )
        mention_map, mention_regex = build_mention_helpers()
        return [serialize_message(m, mention_map, mention_regex) for m in pinned]

    # ---------- Build Broadcast Payload ----------
    @sync_to_async
    def get_message_payload(self, message_id):
        from .models import ChatMessage, CustomUser
        from .utils import serialize_message, build_mention_helpers

        try:
            msg = ChatMessage.objects.select_related("sender", "guest_card", "parent__sender").get(id=message_id)
        except ChatMessage.DoesNotExist:
            return {}

        mention_map, mention_regex = build_mention_helpers()
        return serialize_message(msg, mention_map, mention_regex)

    # ---------- Create Message (Async DB) ----------
    @sync_to_async
    def create_message(
        self, sender_id, message,
        guest_id=None, parent_id=None, mentions_ids=None,
        file_url=None, link_preview=None
    ):
        from .models import ChatMessage, CustomUser
        from guests.models import GuestEntry
        from .utils import serialize_message, build_mention_helpers, get_link_preview
        from django.core.files.storage import default_storage
        import os

        url_pattern = re.compile(r'(https?://[^\s]+)')
        mentions_ids = mentions_ids or []

        try:
            sender = CustomUser.objects.get(id=sender_id)
            guest_card = GuestEntry.objects.filter(id=guest_id).first() if guest_id else None
            parent = ChatMessage.objects.filter(id=parent_id).first() if parent_id else None

            # 🔎 detect link if not provided
            if link_preview:
                link_meta = link_preview
            else:
                link_meta = {}
                match = url_pattern.search(message or "")
                if match:
                    link_meta = get_link_preview(match.group(0))

            # ✅ Cloudinary / Local upload
            file_field = None
            if file_url:
                file_field = handle_file_upload(file_url)

            # ✅ Save message with real FileField
            saved = ChatMessage.objects.create(
                sender=sender,
                message=message or "",
                guest_card=guest_card,
                parent=parent,
                file=file_field,   # 👈 this is now always a FileField
                link_url=link_meta.get("url"),
                link_title=link_meta.get("title"),
                link_description=link_meta.get("description"),
                link_image=link_meta.get("image"),
            )

            # ✅ Serialize
            mention_map, mention_regex = build_mention_helpers()
            return serialize_message(saved, mention_map, mention_regex)

        except Exception as e:
            import logging
            logging.exception("create_message failed: %s", e)
            return {}


# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AttendanceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("attendance", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("attendance", self.channel_name)

    async def send_event(self, event):
        await self.send(text_data=json.dumps(event["data"]))

    async def send_summary(self, summary):
        await self.send(text_data=json.dumps(summary["data"]))


