from .models import MultiloginAccount
from django.contrib.auth.decorators import login_required

@login_required
def get_multilogin_accounts(user):
    return MultiloginAccount.objects.filter(user=user).values()