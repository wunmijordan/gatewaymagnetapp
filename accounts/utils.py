# accounts/utils.py
from django.contrib.auth.models import Group
import requests, mimetypes, os, re, urllib.parse
from bs4 import BeautifulSoup
from .models import CustomUser, ChatMessage
from guests.models import GuestEntry
from .consumers import get_user_color
from django.db.models.fields.files import FieldFile
from django.core.files.storage import default_storage
from django.utils import timezone
from .models import Event, AttendanceRecord
from django.db.models import Q



def user_in_groups(user, group_names):
    """
    Check if a user is superuser OR belongs to any of the provided groups.
    group_names: comma-separated string or list of group names
    """
    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    if isinstance(group_names, str):
        groups = [name.strip() for name in group_names.split(",")]
    else:
        groups = group_names

    return user.groups.filter(name__in=groups).exists()


def get_link_preview(url):
    try:
        resp = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        title = soup.find("meta", property="og:title") or soup.find("title")
        desc = soup.find("meta", property="og:description") or soup.find("meta", attrs={"name": "description"})
        image = soup.find("meta", property="og:image")

        return {
            "url": url,
            "title": title["content"] if title and title.has_attr("content") else (title.text if title else ""),
            "description": desc["content"] if desc and desc.has_attr("content") else "",
            "image": image["content"] if image and image.has_attr("content") else "",
        }
    except Exception:
        return {"url": url, "title": url, "description": "", "image": ""}



def build_mention_helpers():
    """Precompute mention_map + regex for mentions."""
    users = list(CustomUser.objects.all())
    mention_map = {}
    for u in users:
        display = f"@{ (u.title + ' ') if getattr(u, 'title', None) else '' }{ (u.full_name or u.username) }".strip()
        mention_map[display] = u
    regex = re.compile(r"(" + "|".join(map(re.escape, mention_map.keys())) + r")") if mention_map else None
    return mention_map, regex


import os
import urllib
import mimetypes
from django.conf import settings
from django.db.models.fields.files import FieldFile
from django.core.files.storage import default_storage
from guests.models import GuestEntry
from .utils import get_user_color


def serialize_message(m, mention_map=None, mention_regex=None):
    """Unified serializer for both WebSocket + Views."""
    # Mentions
    mentions_payload = []
    if mention_regex and m.message:
        found = set(mention_regex.findall(m.message))
        for token in found:
            u = mention_map.get(token)
            if u:
                mentions_payload.append({
                    "id": u.id,
                    "username": u.username,
                    "title": getattr(u, "title", ""),
                    "name": u.full_name or u.username,
                    "color": get_user_color(u.id),
                })

    # --- Guest
    guest_payload = None
    if m.guest_card:
        g = GuestEntry.objects.select_related("assigned_to").get(id=m.guest_card.id)
        guest_payload = {
            "id": g.id,
            "name": g.full_name,
            "custom_id": g.custom_id,
            "image": g.picture.url if g.picture else None,
            "title": g.title,
            "date_of_visit": g.date_of_visit.strftime("%Y-%m-%d") if g.date_of_visit else "",
            "assigned_user": {
                "id": g.assigned_to.id,
                "title": g.assigned_to.title,
                "full_name": g.assigned_to.full_name,
                "image": g.assigned_to.image.url if g.assigned_to.image else None,
            } if g.assigned_to else None
        }

    # --- Helper to resolve file URLs
    def build_file_payload(file_obj, message_id):
        if not file_obj:
            return None
        try:
            # 1️⃣ For Django FileField (local or CloudinaryField)
            if isinstance(file_obj, FieldFile):
                file_name = urllib.parse.unquote(os.path.basename(file_obj.name))
                file_url = getattr(file_obj, "url", None)

                # Force Cloudinary or media resolution depending on environment
                if not file_url:
                    if settings.DEBUG:
                        file_url = default_storage.url(file_obj.name)
                    else:
                        file_url = f"{settings.MEDIA_URL}{file_obj.name}"

                file_size = getattr(file_obj, "size", None)
                guessed_type, _ = mimetypes.guess_type(file_name)
                file_type = getattr(file_obj.file, "content_type", None) or guessed_type or "application/octet-stream"

            # 2️⃣ If it’s already a Cloudinary or remote URL string
            else:
                file_path = str(file_obj)
                file_name = urllib.parse.unquote(os.path.basename(file_path)) or "file"

                if file_path.startswith("http"):
                    file_url = file_path  # ✅ Cloudinary or remote
                elif settings.DEBUG:
                    file_url = f"/media/{file_path.lstrip('/')}"
                else:
                    # production fallback (Cloudinary path stored as name)
                    file_url = file_path

                file_size = None
                guessed_type, _ = mimetypes.guess_type(file_path)
                file_type = guessed_type or "application/octet-stream"

            return {
                "id": message_id,
                "url": file_url,
                "name": file_name,
                "size": file_size,
                "type": file_type,
            }

        except Exception as e:
            import logging
            logging.warning("serialize_message: file error %s", e)
            return None

    # --- Parent (reply-to)
    parent_payload = None
    if m.parent:
        parent = m.parent
        parent_payload = {
            "id": parent.id,
            "sender_id": parent.sender.id,
            "sender_title": getattr(parent.sender, "title", ""),
            "sender_name": parent.sender.full_name or parent.sender.username,
            "sender_color": get_user_color(parent.sender.id),
            "message": parent.message[:50] if parent.message else "(Attachment)" if parent.file else "(No content)",
            "guest": {
                "id": parent.guest_card.id,
                "name": parent.guest_card.full_name,
                "title": parent.guest_card.title,
                "image": parent.guest_card.picture.url if parent.guest_card.picture else None,
                "date_of_visit": parent.guest_card.date_of_visit.strftime("%Y-%m-%d") if parent.guest_card.date_of_visit else "",
            } if parent.guest_card else None,
            "file": build_file_payload(parent.file, parent.id),
            "link_preview": {
                "url": parent.link_url,
                "title": parent.link_title,
                "description": parent.link_description,
                "image": parent.link_image,
            } if parent.link_url else None,
        }

    # --- File payload (main message)
    file_payload = build_file_payload(m.file, m.id)

    # --- Link preview
    link_payload = None
    if m.link_url:
        link_payload = {
            "url": m.link_url,
            "title": m.link_title,
            "description": m.link_description,
            "image": m.link_image,
        }

    # --- Pinned info
    pinned_by_payload = None
    if getattr(m, "pinned_by", None):
        pinned_by_payload = {
            "id": m.pinned_by.id,
            "name": m.pinned_by.full_name or m.pinned_by.username,
            "title": getattr(m.pinned_by, "title", ""),
        }

    # ✅ Final return
    return {
        "id": m.id,
        "message": m.message,
        "sender_id": m.sender.id,
        "sender_title": getattr(m.sender, "title", ""),
        "sender_name": m.sender.full_name or m.sender.username,
        "sender_image": m.sender.image.url if m.sender.image else None,
        "color": get_user_color(m.sender.id),
        "created_at": m.created_at.isoformat(),
        "guest": guest_payload,
        "reply_to_id": m.parent.id if m.parent else None,
        "parent": parent_payload,
        "file": file_payload,
        "link_preview": link_payload,
        "mentions": mentions_payload,
        "pinned": getattr(m, "pinned", False),
        "pinned_at": m.pinned_at.isoformat() if getattr(m, "pinned_at", None) else None,
        "pinned_by": pinned_by_payload,
    }




def generate_daily_attendance():
    today = timezone.localdate()
    weekday = today.strftime("%A").lower()

    events_today = Event.objects.filter(Q(date=today) | Q(day_of_week=weekday), is_active=True)
    users = CustomUser.objects.filter(is_active=True)

    created_count = 0
    for event in events_today:
        for user in users:
            _, created = AttendanceRecord.objects.get_or_create(
                user=user,
                event=event,
                date=today,
                defaults={"status": "absent"}
            )
            if created:
                created_count += 1
    return created_count


from geopy.distance import distance
from django.core.exceptions import ValidationError
from .models import CHURCH_COORDS

def validate_church_proximity(user_lat, user_lon, threshold_km=0.05):
    """Ensure user is within the threshold distance from church."""
    try:
        # Convert to floats
        lat = float(user_lat)
        lon = float(user_lon)
    except (TypeError, ValueError):
        raise ValidationError("Unable to determine your location. Please enable location access.")

    user_distance = distance(CHURCH_COORDS, (lat, lon)).km

    if user_distance > threshold_km:
        raise ValidationError(
            f"You appear to be {user_distance:.2f} km away from Church. "
            "Please select other options instead."
        )
    print(f"[DEBUG] User distance = {user_distance:.2f} km (Threshold = {threshold_km} km)")



