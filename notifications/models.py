from django.db import models
from users.models import NewUser


class DeliveryLog(models.Model):
  user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
  channel = models.CharField(max_length=20)
  event_type = models.CharField(max_length=50)
  status = models.CharField(max_length=20)
  created_at = models.DateTimeField(auto_now_add=True)
  message = models.TextField(null=True, blank=True)
