from django import forms


class MultiloginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        max_length=255,
        # required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your Multilogin email'
        })
    )
    password = forms.CharField(
        label='Password',
        max_length=255,
        # required=False,  # Không bắt buộc
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )
