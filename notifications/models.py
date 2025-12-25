from django.db import models
from users.models import NewUser


class DeliveryLog(models.Model):
  STATUS_CHOICES = (
    ("pending", "Pending"),
    ("success", "Success"),
    ("failed", "Failed"),
  )

  user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
  channel = models.CharField(max_length=20)
  event_type = models.CharField(max_length=50)
  status = models.CharField(max_length=20, choices=STATUS_CHOICES)
  error_message = models.TextField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  message = models.TextField(null=True, blank=True)


  def __str__(self):
    return f"{self.user.email} | {self.event_type} | {self.channel} | {self.status}"
