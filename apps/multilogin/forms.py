# === django import === #
from django import forms


class MultiloginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
