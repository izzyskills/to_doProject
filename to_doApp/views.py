from django.shortcuts import render, redirect
from . import models, forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.


def home_view(request):
    return render(request, "home.html")


def logoutUser(request):
    logout(request)
    return redirect("home")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            # Perform authentication and login logic here
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")

    return render(request, "login.html", {"form": forms.LoginForm})


def register_view(request):
    logout(request)
    userForm = forms.UserCreationForm()
    context = {"userForm": userForm}
    if request.method == "POST":
        userForm = forms.UserCreationForm(request.POST)
        if userForm.is_valid():
            user = userForm.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect("login")
        else:
            messages.error(request, "an error occurred during Registration ")
    return render(request, "register.html", context)
