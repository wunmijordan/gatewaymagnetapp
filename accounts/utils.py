# accounts/utils.py
from django.contrib.auth.models import Group
import requests, mimetypes, os, re, urllib.parse
from bs4 import BeautifulSoup
from .models import CustomUser, ChatMessage
from guests.models import GuestEntry
from .consumers import get_user_color
from django.db.models.fields.files import FieldFile
from django.core.files.storage import default_storage


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
                    "fullname": u.full_name or u.username,
                    "color": get_user_color(u.id),
                })

    # Guest
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

    # Parent (reply-to)
    parent_payload = None
    if m.parent:
        parent = m.parent
        parent_guest_payload = None
        if parent.guest_card:
            g = parent.guest_card
            parent_guest_payload = {
                "id": g.id,
                "name": g.full_name,
                "title": g.title,
                "image": g.picture.url if g.picture else None,
                "date_of_visit": g.date_of_visit.strftime("%Y-%m-%d") if g.date_of_visit else "",
            }

        # ✅ Choose correct preview text
        if parent.message:
            parent_message_preview = parent.message[:50]
        elif parent.file:
            parent_message_preview = "(Attachment)"
        elif parent.guest_card:
            parent_message_preview = "(Guest Card)"
        elif parent.link_url:
            parent_message_preview = "(Link)"
        else:
            parent_message_preview = "(No content)"

        parent_payload = {
            "id": parent.id,
            "sender_id": parent.sender.id,
            "sender_title": getattr(parent.sender, "title", ""),
            "sender_name": parent.sender.full_name or parent.sender.username,
            "sender_color": get_user_color(parent.sender.id),
            "message": parent_message_preview,
            "guest": parent_guest_payload,
        }

    # File
    file_payload = None
    if m.file:
        try:
            if isinstance(m.file, FieldFile):  # FileField object
                # ✅ Decode filename for display
                file_name = urllib.parse.unquote(os.path.basename(m.file.name))
                file_url = default_storage.url(m.file.name)  # correct URL for frontend
                file_size = getattr(m.file, "size", None)
                guessed_type, _ = mimetypes.guess_type(m.file.name)
                file_type = getattr(m.file.file, "content_type", None) or guessed_type or "application/octet-stream"
            else:  # stored string path
                file_path = str(m.file)
                file_name = urllib.parse.unquote(os.path.basename(file_path)) or "file"
                if not file_path.startswith("/media/"):
                    file_url = f"/media/{file_path.lstrip('/')}"
                else:
                    file_url = file_path
                file_size = None
                guessed_type, _ = mimetypes.guess_type(file_path)
                file_type = guessed_type or "application/octet-stream"

            file_payload = {
                "id": m.id,
                "url": file_url,
                "name": file_name,
                "size": file_size,
                "type": file_type,
            }

        except Exception as e:
            import logging
            logging.warning("serialize_message: file error %s", e)


    # Link
    link_payload = None
    if m.link_url:
        link_payload = {
            "url": m.link_url,
            "title": m.link_title,
            "description": m.link_description,
            "image": m.link_image,
        }

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
    }


