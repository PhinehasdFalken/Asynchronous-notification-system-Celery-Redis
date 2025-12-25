from .email_service import EmailNotificationHandler
from .sms_service import SMSNotificationHandler
from .push_service import PushNotificationHandler


class NotificationFactory:
  @staticmethod
  def get_handler(channel):
    if channel == "email":
      return EmailNotificationHandler()
    elif channel == "sms":
      return SMSNotificationHandler()
    elif channel == "push":
      return PushNotificationHandler()
    raise ValueError("Unsupported notification channel")
