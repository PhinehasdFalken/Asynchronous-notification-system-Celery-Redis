from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .services.factory import NotificationFactory

# the shared_task decorator turns the function below it into a celery task.
# Celery can now run this function in the backgroung insated of Django running it.
@shared_task(bind=True, max_retries=3)
def send_activation_email_task(self, recipient, subject, message):

  send_mail(
    subject, 
    message, 
    settings.DEFAULT_FROM_EMAIL,
    [recipient],
    fail_silently=False,
  )


@shared_task(bind=True, max_retries=3)
def send_notification_task(self, user_id, event_type, channel):
  try:
    handler = NotificationFactory.get_handler(channel)
    handler.send(user_id, event_type)
  except Exception as exc:
    raise self.retry(exc=exc, countdowm=30)
