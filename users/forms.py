from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Імʼя')

    class Meta:
        model = User
        fields = ['first_name', 'username', 'password1', 'password2']
