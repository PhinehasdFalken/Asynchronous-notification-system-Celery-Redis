from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .services.factory import NotificationFactory
from users.models import NewUser
from notifications.models import DeliveryLog

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
  user = NewUser.objects.get(pk=user_id)

  log = DeliveryLog.objects.create(
    user=user,
    event_type=event_type,
    channel=channel,
    status="pending",
  )

  try:
    handler = NotificationFactory.get_handler(channel)
    handler.send(user_id, event_type)

    log.status = "success"
    log.save(update_fields=["status"])

  except Exception as exc:
    log.status = "failed"
    log.error_message = str(exc)
    log.save(update_fields=["status", "error_message"])
    
    raise self.retry(exc=exc, countdowm=30)
