from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


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
    multilogin_profile_name = models.CharField(max_length=255, default="")

    class Meta:
        unique_together = None


class Action(models.Model):
    ACTION_TYPES = [
        ('visit_website', 'Truy cập Website'),
        ('scroll_up', 'Cuộn lên'),
        ('scroll_down', 'Cuộn xuống'),
        ('watch_video', 'Xem Video'),
        ('click_position', 'Click vào vị trí bất kỳ (x,y)'),
        ('click', 'Click chọn (css_selectors)'),
        ('scroll_start', 'Cuộn đến đầu trang'),
        ('scroll_end', 'Cuộn đến cuối trang'),
    ]

    name = models.CharField(max_length=255)
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES)
    action_func = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.action_type


class Script(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ScriptStep(models.Model):
    script = models.ForeignKey(
        Script, on_delete=models.CASCADE, related_name='steps')
    action = models.ForeignKey(Action, on_delete=models.SET_NULL, null=True)
    step_order = models.IntegerField()
    # delay = models.IntegerField(default=10)
    # status = models.BooleanField(default=True)
    parameters = models.JSONField()  # Store action-specific parameters here
    created = models.DateTimeField(auto_now_add=True)
