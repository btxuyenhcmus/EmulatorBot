from django.contrib import admin
from .models import User, Action, Script, ScriptStep, MultiloginAccount
# Register your models here.
admin.site.register(User)
admin.site.register(Action)
admin.site.register(Script)
admin.site.register(ScriptStep)
admin.site.register(MultiloginAccount)
