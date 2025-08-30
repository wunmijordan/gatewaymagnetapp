from django import template

register = template.Library()

@register.filter
def status_color(value):
    return {
        'select_status': 'primary',
        'planted': 'secondary',
        'planted_elsewhere': 'success',
        'relocated': 'danger',
        'work_in_progress': 'warning',
    }.get(value, 'primary')  # Default to primary if status not recognized


@register.filter
def attr(obj, field_name):
    """
    Safely get an attribute from a model instance or a dict.
    Returns None if not found.
    """
    if isinstance(obj, dict):
        return obj.get(field_name)
    return getattr(obj, field_name, None)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
