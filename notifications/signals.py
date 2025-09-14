from django.db.models.signals import post_save, post_delete
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserSettings, Notification
from guests.models import Review, GuestEntry
from accounts.models import ChatMessage
from django.urls import reverse
from notifications.middleware import get_current_user
from django.utils import timezone
from accounts.utils import user_in_groups
from notifications.utils import (
    notify_users,
    STAFF_GROUPS,
    guest_full_name,
    user_full_name,
    get_user_role,
)


User = get_user_model()


# -----------------------------
# Guest Signals
# -----------------------------
@receiver(post_save, sender=GuestEntry)
def notify_guest_creation(sender, instance, created, **kwargs):
    if not created:
        return

    registrant = get_current_user()  # use currently logged-in user

    ts = timezone.localtime().strftime("%Y-%m-%d %H:%M:%S")
    guest_name = guest_full_name(instance)
    creator_name = user_full_name(registrant)
    custom_id = getattr(instance, "custom_id", "N/A")
    guest_count = GuestEntry.objects.count()
    superusers = User.objects.filter(is_superuser=True)
    staff_users = User.objects.filter(groups__name__in=STAFF_GROUPS).exclude(is_superuser=True).distinct()

    description = (
        f"{guest_name} ({custom_id})\n"
        f"Registered by: {creator_name}, at {ts}.\n"
        f"New Guests Count: {guest_count}"
    )
    link = reverse("guest_list")

    notify_users(superusers, "Guest Created", description, link, is_success=True)
    notify_users(staff_users, "Guest Created", description, link, is_success=True)


@receiver(post_delete, sender=GuestEntry)
def notify_guest_deletion(sender, instance, **kwargs):
    deleter = get_current_user()

    ts = timezone.localtime().strftime("%Y-%m-%d %H:%M:%S")
    guest_name = guest_full_name(instance)
    deleter_name = user_full_name(deleter)
    custom_id = getattr(instance, "custom_id", "N/A")
    guest_count = GuestEntry.objects.count()
    superusers = User.objects.filter(is_superuser=True)
    staff_users = User.objects.filter(groups__name__in=STAFF_GROUPS).exclude(is_superuser=True).distinct()

    description = (
        f"{guest_name} ({custom_id})\n"
        f"Deleted by: {deleter_name}, at {ts}.\n"
        f"New Guests Count: {guest_count}"
    )
    link = reverse("guest_list")

    notify_users(superusers, "Guest Deleted", description, link, is_urgent=True)
    notify_users(staff_users, "Guest Deleted", description, link, is_urgent=True)


@receiver(post_save, sender=GuestEntry)
def notify_guest_assignment(sender, instance, created, **kwargs):
    if created:
        return
    if instance.assigned_to:
        ts = timezone.localtime().strftime("%Y-%m-%d %H:%M:%S")
        guest_name = guest_full_name(instance)
        assigned_user = instance.assigned_to
        assigned_user_name = user_full_name(assigned_user)  # display string
        self_msg = f"I have been assigned: {guest_name} ({instance.custom_id}), at {ts}."
        others_msg = f"{assigned_user_name} has been assigned: {guest_name} ({instance.custom_id}), at {ts}."
        superusers = User.objects.filter(is_superuser=True).exclude(id=assigned_user.id)
        staff_users = User.objects.filter(groups__name__in=STAFF_GROUPS).exclude(
            id__in=[assigned_user.id]
        ).exclude(is_superuser=True).distinct()
        link = reverse("guest_list")

        notify_users([instance.assigned_to], "Guest Assigned", self_msg, link, is_success=True)
        notify_users(superusers, "Guest Assigned", others_msg, link, is_urgent=True)
        notify_users(staff_users, "Guest Assigned", others_msg, link, is_success=True)



@receiver(post_save, sender=Review)
def notify_review_submission(sender, instance, created, **kwargs):
    if not created:
        return

    reviewer = instance.reviewer
    guest = instance.guest
    ts = timezone.localtime().strftime("%Y-%m-%d %H:%M:%S")
    guest_name = guest_full_name(guest)
    reviewer_name = user_full_name(reviewer)
    link = reverse("guest_list")  # adjust if you have review detail page

    # -----------------------------
    # Determine recipients
    # -----------------------------
    # Superusers: always notified (exclude reviewer)
    superusers = User.objects.filter(is_superuser=True).exclude(id=reviewer.id)

    # Staff users: exclude reviewer and superusers
    staff_users = User.objects.filter(groups__name__in=STAFF_GROUPS).exclude(id=reviewer.id).exclude(is_superuser=True).distinct()

    # Guest owner / assigned user
    guest_owner = []
    if guest.assigned_to and guest.assigned_to != reviewer:
        guest_owner = [guest.assigned_to]

    # -----------------------------
    # If this review is a reply, exclude parent reviewer from general notification
    # -----------------------------
    parent_reviewer = None
    if instance.parent and instance.parent.reviewer != reviewer:
        parent_reviewer = instance.parent.reviewer
        if parent_reviewer in superusers:
            superusers = superusers.exclude(id=parent_reviewer.id)
        if parent_reviewer in staff_users:
            staff_users = staff_users.exclude(id=parent_reviewer.id)
        if parent_reviewer in guest_owner:
            guest_owner = []

    # Combine recipients
    recipients = list({user.id: user for user in list(superusers) + list(staff_users) + guest_owner}.values())

    # -----------------------------
    # Send general notification
    # -----------------------------
    if recipients:
        notify_users(
            recipients,
            "Review Submitted",
            f"{reviewer_name} submitted a review for {guest_name}, at {ts}.",
            link,
            is_success=True
        )

    # -----------------------------
    # Send reply notification (always "Review Reply")
    # -----------------------------
    if parent_reviewer:
        parent_msg = f"{reviewer_name} replied to your review for {guest_name}, at {ts}."
        notify_users([parent_reviewer], "Review Reply", parent_msg, link, is_success=True)




# -----------------------------
# User Signals
# -----------------------------
@receiver(post_save, sender=User)
def notify_user_creation(sender, instance, created, **kwargs):
    if not created:
        return
    ts = timezone.localtime().strftime("%Y-%m-%d %H:%M:%S")
    superusers = User.objects.filter(is_superuser=True)
    staff_users = User.objects.filter(groups__name__in=STAFF_GROUPS).exclude(is_superuser=True).distinct()
    description = f"New user created: {user_full_name(instance)}, at {ts}."
    link = reverse("accounts:user_list")

    notify_users(superusers, "User Created", description, link, is_success=True)
    notify_users(staff_users, "User Created", description, link, is_success=True)


@receiver(post_delete, sender=User)
def notify_user_deletion(sender, instance, **kwargs):
    ts = timezone.localtime().strftime("%Y-%m-%d %H:%M:%S")
    superusers = User.objects.filter(is_superuser=True)
    staff_users = User.objects.filter(groups__name__in=STAFF_GROUPS).exclude(is_superuser=True).distinct()
    description = f"User deleted: {user_full_name(instance)}, at {ts}."
    link = reverse("accounts:user_list")

    notify_users(superusers, "User Deleted", description, link, is_urgent=True)
    notify_users(staff_users, "User Deleted", description, link, is_urgent=True)


@receiver(user_logged_in)
def notify_user_login(sender, request, user, **kwargs):
    ts = timezone.localtime().strftime("%Y-%m-%d %H:%M:%S")
    user_name = user_full_name(user)
    role = get_user_role(user)
    description_self = f"I just logged in at {ts}."
    description_others = f"{user_name} logged in at {ts}."
    link = reverse("accounts:user_list")

    # Superuser sees everything
    if user.is_superuser:
        notify_users([user], "User Login", description_self, link, is_urgent=True)
    # Staff login
    elif user_in_groups(user, STAFF_GROUPS):
        # Notify self
        notify_users([user], "User Login", description_self, link, is_urgent=True)
        # Notify other staff in same groups, excluding self
        others = User.objects.filter(groups__name__in=STAFF_GROUPS).exclude(id=user.id)
        # Superusers also see
        superusers = User.objects.filter(is_superuser=True)
        notify_users(list(others) + list(superusers), "User Login", description_others, link, is_urgent=True)
    # Regular user login
    else:
        # Notify staff + superusers
        recipients = User.objects.filter(groups__name__in=STAFF_GROUPS) | User.objects.filter(is_superuser=True)
        notify_users(recipients.distinct(), "User Login", description_others, link, is_urgent=True)




@receiver(post_save, sender=ChatMessage)
def create_chat_notification(sender, instance, created, **kwargs):
    if not created:
        return

    sender_user = instance.sender
    message_preview = instance.message[:50] or "(Attachment)"
    ts = timezone.localtime(instance.created_at).strftime("%Y-%m-%d %H:%M:%S")
    link = reverse("accounts:chat_room")  # your chat page url name

    recipients = User.objects.exclude(id=sender_user.id)

    description = (
        f"{sender_user.full_name or sender_user.username}:\n"
        f"{message_preview}.\n"
        f"{ts}"
    )

    notify_users(
        recipients,
        "ChatRoom",
        description,
        link,
        is_success=True
    )





@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):
    if created:
        UserSettings.objects.create(user=instance)
