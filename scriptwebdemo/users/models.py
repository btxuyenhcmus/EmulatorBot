from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=25, default="")
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
class MultiloginAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    multilogin_email = models.EmailField(unique=False)
    multilogin_password = models.CharField(max_length=1024)
    multilogin_token = models.CharField(max_length=1024)
    multilogin_folder_id = models.CharField(max_length=255)
    multilogin_profile_id = models.CharField(max_length=255)
    multilogin_profile_name = models.CharField(max_length=255 , default="")
    class Meta:
     unique_together = ('user', 'multilogin_email')