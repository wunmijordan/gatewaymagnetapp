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
