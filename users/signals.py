from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import NewUser, Profile
# from notifications.tasks import send_notification_task

# @receiver(post_save, sender=NewUser)
# def notify_on_signup(sender, instance, created, **kwargs):
#     if created:
#         send_notification_task.delay(
#             user_id=instance.id,
#             event_type="user_signup",
#             channel="email"
#     )

@receiver(post_save, sender=NewUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=NewUser)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
