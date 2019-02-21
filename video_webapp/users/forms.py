# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import CustomUser, Profile
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):

  class Meta(UserCreationForm):
    model = CustomUser
    fields = ('username',)

class CustomUserChangeForm(forms.ModelForm):

  class Meta:
    model = CustomUser
    fields = ('username',)

class ProfileUpdateForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ('image',)

class UserChangePasswordForm(PasswordChangeForm):
  class Meta:
    model = get_user_model()
    fields = ('password',)