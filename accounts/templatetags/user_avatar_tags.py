from django import template
from django.utils.html import format_html

register = template.Library()

@register.simple_tag
def render_user_avatar(user, size="avatar-sm"):
    """
    Render a user avatar with profile image or fallback to initials.
    'size' is optional for CSS avatar size class.
    """
    profile = getattr(user, 'profile', None)
    if profile and profile.image and hasattr(profile.image, 'url'):
        return format_html(
            '<span class="avatar {}" style="background-image: url(\'{}\');"></span>',
            size,
            profile.image.url
        )
    else:
        initials = ''
        if profile and hasattr(profile, 'initials'):
            initials = profile.initials
        else:
            full_name = user.get_full_name()
            if full_name:
                initials = ''.join([name[0].upper() for name in full_name.split()])
            else:
                initials = user.username[0].upper()
        
        return format_html(
            '<span class="avatar {} bg-secondary text-white d-flex align-items-center justify-content-center fw-bold">{}</span>',
            size,
            initials
        )
