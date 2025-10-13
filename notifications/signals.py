from django.db.models.signals import pre_save, post_save, post_delete
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserSettings, Notification, PushSubscription
from guests.models import Review, GuestEntry
from accounts.models import ChatMessage
from django.urls import reverse
from notifications.middleware import get_current_user
from django.utils import timezone
from accounts.utils import user_in_groups
from .utils import notify_users
from pywebpush import WebPushException
import re
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
@receiver(pre_save, sender=GuestEntry)
def cache_old_assignment(sender, instance, **kwargs):
    """
    Store the current assigned_to before saving so we can detect reassignment.
    """
    if instance.pk:
        try:
            old = sender.objects.get(pk=instance.pk)
            instance._old_assigned_to = old.assigned_to
        except sender.DoesNotExist:
            instance._old_assigned_to = None
    else:
        instance._old_assigned_to = None


@receiver(post_save, sender=GuestEntry)
def notify_guest_creation_or_assignment(sender, instance, created, **kwargs):
    """
    Sends notifications for:
    - New guest creation
    - Guest assignment
    - Guest reassignment
    """
    ts = timezone.localtime().strftime("%b. %d, %Y - %H:%M")
    guest_name = guest_full_name(instance)
    custom_id = getattr(instance, "custom_id", "N/A")
    link = reverse("guest_list")
    registrant = get_current_user()  # implement properly
    creator_name = user_full_name(registrant)

    old_assigned = getattr(instance, "_old_assigned_to", None)
    new_assigned = instance.assigned_to

    # --- CASE 1: New guest ---
    if created:
        # Top-level notification for superusers and staff (excluding assignee)
        top_level_msg = (
            f"{guest_name} ({custom_id})\n"
            f"Registered by: {creator_name}, at {ts}.\n"
            f"New Guests Count: {GuestEntry.objects.count()}."
        )
        if new_assigned:
            assigned_user_name = user_full_name(new_assigned)
            top_level_msg += f"\nAssigned to: {assigned_user_name}."

        superusers = User.objects.filter(is_superuser=True)
        staff_users = User.objects.filter(groups__name__in=STAFF_GROUPS).exclude(is_superuser=True).distinct()
        if new_assigned:
            top_level_recipients = list(superusers.exclude(id=new_assigned.id)) + \
                                   list(staff_users.exclude(id=new_assigned.id))
        else:
            top_level_recipients = list(superusers) + list(staff_users)

        notify_users(top_level_recipients, "Guest Created", top_level_msg, link, is_success=True)

        # Notify assigned user
        if new_assigned:
            assigned_msg = f"I have been assigned: {guest_name} ({custom_id}), at {ts}."
            notify_users([new_assigned], "Guest Assigned", assigned_msg, link, is_success=True)

        return  # done with creation

    # --- CASE 2: Guest reassignment ---
    if old_assigned != new_assigned:
        # Notify new assignee
        if new_assigned:
            assigned_msg = f"I have been reassigned: {guest_name} ({custom_id}), at {ts}."
            notify_users([new_assigned], "Guest Reassigned", assigned_msg, link, is_success=True)

        # Notify top-level roles
        others_msg = (
            f"{guest_name} ({custom_id}) has been reassigned "
            f"to {user_full_name(new_assigned) if new_assigned else 'no one'}, at {ts}."
        )
        superusers = User.objects.filter(is_superuser=True)
        if new_assigned:
            superusers = superusers.exclude(id=new_assigned.id)
        staff_users = User.objects.filter(groups__name__in=STAFF_GROUPS)\
                                  .exclude(is_superuser=True)
        if new_assigned:
            staff_users = staff_users.exclude(id=new_assigned.id)
        staff_users = staff_users.distinct()

        notify_users(list(superusers) + list(staff_users), "Guest Reassigned", others_msg, link, is_urgent=True)

    # --- CASE 3: Guest edited, assignment unchanged ---
    # Do nothing




@receiver(post_delete, sender=GuestEntry)
def notify_guest_deletion(sender, instance, **kwargs):
    deleter = get_current_user()

    ts = timezone.localtime().strftime("%b. %d, %Y - %H:%M")
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



@receiver(post_save, sender=Review)
def notify_review_submission(sender, instance, created, **kwargs):
    if not created:
        return

    reviewer = instance.reviewer
    guest = instance.guest
    ts = timezone.localtime().strftime("%b. %d, %Y - %H:%M")
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
    ts = timezone.localtime().strftime("%b. %d, %Y - %H:%M")
    superusers = User.objects.filter(is_superuser=True)
    staff_users = User.objects.filter(groups__name__in=STAFF_GROUPS).exclude(is_superuser=True).distinct()
    description = f"New user created: {user_full_name(instance)}, at {ts}."
    link = reverse("accounts:user_list")

    notify_users(superusers, "User Created", description, link, is_success=True)
    notify_users(staff_users, "User Created", description, link, is_success=True)


@receiver(post_delete, sender=User)
def notify_user_deletion(sender, instance, **kwargs):
    ts = timezone.localtime().strftime("%b. %d, %Y - %H:%M")
    superusers = User.objects.filter(is_superuser=True)
    staff_users = User.objects.filter(groups__name__in=STAFF_GROUPS).exclude(is_superuser=True).distinct()
    description = f"User deleted: {user_full_name(instance)}, at {ts}."
    link = reverse("accounts:user_list")

    notify_users(superusers, "User Deleted", description, link, is_urgent=True)
    notify_users(staff_users, "User Deleted", description, link, is_urgent=True)


@receiver(user_logged_in)
def notify_user_login(sender, request, user, **kwargs):
    ts = timezone.localtime().strftime("%b. %d, %Y - %H:%M")
    user_name = user_full_name(user)
    role = get_user_role(user)
    description_self = f"I just logged in, at {ts}."
    description_others = f"{user_name} logged in, at {ts}."
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



def escape_regex(string):
    if not string:
        return ""
    return re.escape(string)

def detect_mentions_from_text(text):
    """
    Detects mentions in a message, considering @Title FullName.
    Returns a queryset of User objects mentioned.
    """
    if not text:
        return User.objects.none()

    users = User.objects.all()
    mentioned_users = []
    for u in users:
        full_name = escape_regex(u.full_name or u.username)
        title = escape_regex(u.title) if u.title else ""
        if title:
            pattern = rf"@(?:{title}\s+)?{full_name}"
        else:
            pattern = rf"@{full_name}"
        if re.search(pattern, text, re.IGNORECASE):
            mentioned_users.append(u)
    return User.objects.filter(id__in=[u.id for u in mentioned_users])

@receiver(pre_save, sender=ChatMessage)
def cache_old_pin(sender, instance, **kwargs):
    """
    Cache the old pinned status and pinner for comparison.
    """
    if instance.pk:
        old = sender.objects.filter(pk=instance.pk).first()
        instance._old_pinned = old.pinned if old else False
        instance._old_pinned_by = old.pinned_by if old else None
    else:
        instance._old_pinned = False
        instance._old_pinned_by = None

@receiver(post_save, sender=ChatMessage)
def create_chat_notification(sender, instance, created, **kwargs):
    sender_user = instance.sender
    just_pinned = instance.pinned and (getattr(instance, "_old_pinned", False) == False)
    # Use pin time if message was just pinned, else original creation time
    ts = timezone.localtime(instance.pinned_at if just_pinned else instance.created_at).strftime("%b. %d, %Y - %H:%M")
    link = reverse("accounts:chat_room")

    message_preview = "(No content)"
    if instance.message:
        message_preview = instance.message[:50]
    elif instance.file:
        message_preview = "(Attachment)"
    elif instance.guest_card:
        message_preview = f"(Guest: {instance.guest_card.full_name})"

    notified_users = set()

    # -----------------------------
    # 1️⃣ Handle newly pinned messages
    # -----------------------------
    if just_pinned and instance.pinned_by:
        # Detect mentioned users in the message
        mentioned_users = detect_mentions_from_text(instance.message)
        mentioned_ids = [u.id for u in mentioned_users]

        # Pinner gets their own notification
        notify_users(
            [instance.pinned_by],
            "Pinned Message",
            f"I pinned a message, at {ts}",
            link,
            is_success=True
        )
        notified_users.add(instance.pinned_by.id)

        # Mentioned users get a modified notification
        for u in mentioned_users:
            notify_users(
                [u],
                "Pinned Message",
                f"{user_full_name(instance.pinned_by)} pinned a message I was mentioned in, at {ts}",
                link,
                is_success=True
            )
            notified_users.add(u.id)

        # Everyone else (exclude pinner + mentioned)
        other_users = User.objects.exclude(id__in=notified_users)
        notify_users(
            other_users,
            "Pinned Message",
            f"{user_full_name(instance.pinned_by)} pinned a message, at {ts}",
            link,
            is_success=True
        )
        notified_users.update(u.id for u in other_users)

    # -----------------------------
    # 2️⃣ Handle mentions (only if not just pinned)
    # -----------------------------
    if instance.message and not just_pinned:
        mentioned_users = detect_mentions_from_text(instance.message)

        for user in mentioned_users:
            notify_users(
                [user],
                "Mentioned",
                f"{user_full_name(sender_user)} mentioned me in a message, at {ts}",
                link,
                is_success=True
            )
            notified_users.add(user.id)

        # Sender notification
        mentioned_names_list = [user_full_name(u) for u in mentioned_users]
        if sender_user in mentioned_users:
            mentioned_names_list.remove(user_full_name(sender_user))
            mentioned_names_list = ["myself"] + mentioned_names_list

        if mentioned_names_list:
            notify_users(
                [sender_user],
                "Mentioned",
                f"I mentioned {', '.join(mentioned_names_list)} in a message, at {ts}",
                link,
                is_success=True
            )
            notified_users.add(sender_user.id)

        # Top-level users (superuser, Pastor, Team Lead, Admin)
        top_level_users = User.objects.filter(groups__name__in=STAFF_GROUPS).exclude(id__in=notified_users).distinct()
        if top_level_users.exists() and mentioned_users:
            top_level_names = ", ".join([user_full_name(u) for u in mentioned_users])
            notify_users(
                list(top_level_users),
                "Mentioned",
                f"{user_full_name(sender_user)} mentioned {top_level_names} in a message, at {ts}",
                link,
                is_success=True
            )
            notified_users.update(u.id for u in top_level_users)

    # -----------------------------
    # 3️⃣ Regular chat notification for remaining users
    # -----------------------------
    remaining_recipients = User.objects.exclude(id__in=notified_users)
    if remaining_recipients.exists():
        notify_users(
            remaining_recipients,
            "ChatRoom",
            f"{user_full_name(sender_user)}:\n{message_preview}.\n{ts}",
            link,
            is_success=True
        )



@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):
    if created:
        UserSettings.objects.create(user=instance)


"""
@receiver(post_save, sender=Notification)
def push_on_notification(sender, instance, created, **kwargs):
    if created:
        subscriptions = PushSubscription.objects.filter(user=instance.user)
        for sub in subscriptions:
            try:
                send_push(
                    sub.subscription_data,
                    title=instance.title,
                    body=instance.description,
                    url=instance.link or "/"
                )
            except WebPushException as e:
                if "410" in str(e) or "404" in str(e):
                    # subscription expired → remove it
                    sub.delete()
                else:
                    print("Push failed:", repr(e))
"""

