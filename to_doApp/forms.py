from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . import models


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password1", "password2"]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ["name", "description", "category", "date", "recurrence"]


class CategoryCreationForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ["name"]
