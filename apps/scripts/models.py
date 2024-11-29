from django.db import models
from django.conf import settings


class Script(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ScriptStep(models.Model):
    script = models.ForeignKey(
        Script, on_delete=models.CASCADE, related_name='steps')
    action = models.CharField(max_length=255)
    step_order = models.IntegerField()
    parameters = models.JSONField()
    created = models.DateTimeField(auto_now_add=True)
