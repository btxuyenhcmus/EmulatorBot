from django.db import models
from django.conf import settings


class MultiloginAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    email = models.EmailField(unique=False)
    password = models.CharField(max_length=1024)
    folder_id = models.CharField(max_length=255)
    profile_id = models.CharField(max_length=255)
    profile_name = models.CharField(max_length=255, default="")

    class Meta:
        unique_together = None
