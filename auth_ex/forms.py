from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


User = get_user_model()


class LogInForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'password']


class UserDetailsForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'nick', 'phone_number', 'ice_contact_name', 'ice_contact_number', 'birth_date', ]


class VerifyPasswordForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['password',]


class ChageEmailForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email',]
