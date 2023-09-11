from collections.abc import Mapping
from typing import Any
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
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
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, user, *args, **kwargs):
        super(TaskCreationForm, self).__init__(*args, **kwargs)
        self.fields["category"].queryset = models.Category.objects.filter(user=user)


class CategoryCreationForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if " " in name:
            raise forms.ValidationError("Category names cannot contain spaces.")
        return name
