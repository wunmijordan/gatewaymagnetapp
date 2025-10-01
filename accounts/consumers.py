import json
import logging
from datetime import timedelta
from django.utils.timezone import now
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

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
            action = data.get("action")
            if action:
                await self.handle_action(data)
                return

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
        message = data.get("message", "").strip()
        guest_id = data.get("guest_id")
        parent_id = data.get("reply_to_id")
        mentions_ids = data.get("mentions", [])

        if not message and not guest_id:
            return

        saved_message = await self.create_message(sender_id, message, guest_id, parent_id, mentions_ids)
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
        return [self.serialize_message(m) for m in pinned]

    def serialize_message(self, m):
        """Enriched payload for pinned preview"""
        return {
            "id": m.id,
            "message": m.message[:50],
            "original_sender_id": m.sender.id,
            "original_sender_name": m.sender.full_name or m.sender.username,
            "original_sender_title": getattr(m.sender, "title", ""),
            "pinned": m.pinned,
            "pinned_at": m.pinned_at.isoformat() if m.pinned_at else None,
            "pinned_by": {
                "id": m.pinned_by.id if m.pinned_by else None,
                "name": (m.pinned_by.full_name or m.pinned_by.username) if m.pinned_by else None,
                "title": getattr(m.pinned_by, "title", "") if m.pinned_by else "",
            } if m.pinned_by else None,
            "guest": {
                "id": m.guest_card.id,
                "name": m.guest_card.full_name,
                "title": m.guest_card.title,
                "image": m.guest_card.picture.url if m.guest_card.picture else None,
            } if m.guest_card else None,
        }

    # ---------- Build Broadcast Payload ----------
    @sync_to_async
    def get_message_payload(self, message_id):
        from .models import ChatMessage, CustomUser
        try:
            m = ChatMessage.objects.select_related("sender", "guest_card", "parent__sender").get(id=message_id)
        except ChatMessage.DoesNotExist:
            return {}

        payload = {
            "id": m.id,
            "message": m.message,
            "created_at": m.created_at.isoformat(),
            "sender_id": m.sender.id,
            "sender_title": getattr(m.sender, "title", ""),
            "sender_name": m.sender.full_name or m.sender.username,
            "sender_image": m.sender.image.url if getattr(m.sender, "image", None) else None,
            "guest": None,
            "parent": None,
            "pinned": getattr(m, "pinned", False),
            "color": get_user_color(m.sender.id),
        }

        if m.guest_card:
            g = m.guest_card
            payload["guest"] = {
                "id": g.id,
                "name": g.full_name,
                "custom_id": g.custom_id,
                "image": g.picture.url if g.picture else None,
                "title": g.title,
                "date_of_visit": g.date_of_visit.strftime("%Y-%m-%d") if g.date_of_visit else ""
            }

        if m.parent:
            p = m.parent
            payload["parent"] = {
                "id": p.id,
                "sender_title": getattr(p.sender, "title", ""),
                "sender_name": p.sender.full_name or p.sender.username,
                "message": p.message[:50]
            }

        # mentions
        mentions_payload = []
        try:
            if hasattr(m, "mentions_ids") and m.mentions_ids:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                ids = [int(i) for i in m.mentions_ids]
                for u in User.objects.filter(id__in=ids):
                    mentions_payload.append({
                        "id": u.id,
                        "username": u.username,
                        "title": getattr(u, "title", ""),
                        "fullname": u.full_name or u.username
                    })
        except Exception:
            logger.debug("No mentions found for message %s", m.id)

        payload["mentions"] = mentions_payload
        return payload

    # ---------- Create Message (Async DB) ----------
    @sync_to_async
    def create_message(self, sender_id, message, guest_id=None, parent_id=None, mentions_ids=None):
        from .models import ChatMessage, CustomUser
        from guests.models import GuestEntry
        mentions_ids = mentions_ids or []

        try:
            sender = CustomUser.objects.get(id=sender_id)
            guest_card = GuestEntry.objects.filter(id=guest_id).first() if guest_id else None
            parent = ChatMessage.objects.filter(id=parent_id).first() if parent_id else None

            saved = ChatMessage.objects.create(sender=sender, message=message,
                                               guest_card=guest_card, parent=parent)

            payload = {
                "id": saved.id,
                "message": saved.message,
                "created_at": saved.created_at.isoformat(),
                "sender_id": sender.id,
                "sender_title": getattr(sender, "title", ""),
                "sender_name": sender.full_name or sender.username,
                "sender_image": sender.image.url if getattr(sender, "image", None) else None,
                "guest": None,
                "parent": None,
                "reply_to_id": parent.id if parent else None,
                "pinned": getattr(saved, "pinned", False),
                "color": get_user_color(sender.id),
            }

            if guest_card:
                payload["guest"] = {
                    "id": guest_card.id,
                    "name": guest_card.full_name,
                    "custom_id": guest_card.custom_id,
                    "image": guest_card.picture.url if guest_card.picture else None,
                    "title": guest_card.title,
                    "date_of_visit": guest_card.date_of_visit.strftime("%Y-%m-%d") if guest_card.date_of_visit else ""
                }

            if parent:
                parent_data = {
                    "id": parent.id,
                    "sender_title": getattr(parent.sender, "title", ""),
                    "sender_name": parent.sender.full_name or parent.sender.username,
                    "message": parent.message[:50]
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

            # mentions resolution
            mentions_payload = []
            if mentions_ids:
                try:
                    ids = [int(i) for i in mentions_ids]
                except Exception:
                    ids = []
                if ids:
                    for u in CustomUser.objects.filter(id__in=ids):
                        mentions_payload.append({
                            "id": u.id,
                            "username": u.username,
                            "title": getattr(u, "title", ""),
                            "fullname": u.full_name or u.username
                        })
            else:
                # fallback detection
                for u in CustomUser.objects.all():
                    display = f"@{ (u.title + ' ') if getattr(u, 'title', None) else '' }{ (u.full_name or u.username) }".strip()
                    if display in message:
                        mentions_payload.append({
                            "id": u.id,
                            "username": u.username,
                            "title": getattr(u, "title", ""),
                            "fullname": u.full_name or u.username
                        })

            payload["mentions"] = mentions_payload
            return payload

        except Exception as e:
            logger.exception("create_message failed: %s", e)
            return {}
