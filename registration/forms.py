from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm 

User=get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'is_staff')


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'password',
            'first_name',
            'last_name',
            'nick',
            'phone_number',
            'ice_contact_name',
            'ice_contact_number',
            'birth_date',
            )
