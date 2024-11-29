# === django import === #
from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    password = models.CharField()


class Profile(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    folder = models.CharField()
    profile = models.CharField()
    name = models.CharField(null=True, blank=True)
