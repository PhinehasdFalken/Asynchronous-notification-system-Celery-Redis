from django.core.mail import send_mail
from django.conf import settings
from users.models import NewUser


class EmailNotificationHandler:
  def send(self, user_id, event_type):
    user = NewUser.objects.get(pk=user_id)
    subject = "Welcome!" if event_type == "user_signup" else "Notification"
    message = f"Hi {user.user_name}, thanks for signing up!"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
    print(f"✅ Email sent to {user.email}")
