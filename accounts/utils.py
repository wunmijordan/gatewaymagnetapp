# accounts/utils.py
from django.contrib.auth.models import Group

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
