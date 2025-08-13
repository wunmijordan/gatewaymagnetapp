from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if dictionary and key:
        return dictionary.get(key)
    return ''

@register.filter
def detect_social_media_type(handle_url):
    """
    Detect social media platform from a full URL or raw handle.
    Returns one of: 'linkedin', 'whatsapp', 'instagram', 'twitter', 'tiktok', or ''.
    """
    if not handle_url:
        return ''

    url = handle_url.strip().lower()

    # Map known base URLs to platform keys
    base_urls = {
        'linkedin.com': 'linkedin',
        'wa.me': 'whatsapp',
        'whatsapp.com': 'whatsapp',
        'instagram.com': 'instagram',
        'twitter.com': 'twitter',
        'tiktok.com': 'tiktok'
    }

    # Match known URLs
    for base, platform in base_urls.items():
        if base in url:
            return platform

    # Optional: detect raw handles by assuming platform prefix
    for platform in ['linkedin', 'whatsapp', 'instagram', 'twitter', 'tiktok']:
        if url.startswith(platform):
            return platform

    return ''  # fallback
