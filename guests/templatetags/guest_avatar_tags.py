from django import template
from django.utils.html import format_html

register = template.Library()

@register.simple_tag
def render_guest_avatar(guest, size="avatar-md"):
    """
    Renders a guest avatar with picture or fallback to initials.
    'size' is an optional CSS class for avatar sizing.
    """
    if guest.picture and hasattr(guest.picture, 'url'):
        return format_html(
            '<span class="avatar {}" style="background-image: url(\'{}\');"></span>',
            size,
            guest.picture.url
        )
    else:
        initials = guest.initials or "?"
        return format_html(
            '<span class="avatar {} bg-primary text-white d-flex align-items-center justify-content-center fw-bold">{}</span>',
            size,
            initials
        )
