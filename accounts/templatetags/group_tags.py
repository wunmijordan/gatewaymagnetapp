# accounts/templatetags/group_tags.py
from django import template
from accounts.utils import user_in_groups

register = template.Library()

@register.filter
def has_group(user, group_names):
    return user_in_groups(user, group_names)
