from django.shortcuts import render, redirect, get_object_or_404
from . import models, forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone

# Create your views here.


def home_view(request):
    return render(request, "index.html")


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
            username = form.cleaned_data["username"].lower()
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
            else:
                messages.error(request, "an error occurred during Authentication ")

    return render(request, "login.html", {"form": forms.LoginForm})


def register_view(request):
    logout(request)
    form = forms.UserCreationForm()
    context = {"form": form}
    if request.method == "POST":
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect("login")
        else:
            messages.error(request, "an error occurred during Registration ")
    return render(request, "register.html", context)


@login_required(login_url="login")
def dashboard_view(request):
    categories = models.Category.objects.filter(user=request.user)
    today = timezone.now().date()
    overdue_tasks = models.Task.objects.filter(user=request.user, date__lt=today)
    today_tasks = models.Task.objects.filter(user=request.user, date=today)
    dashboard_task_count = today_tasks.count() + overdue_tasks.count()

    return render(
        request,
        "dashboard.html",
        {
            "overdue_tasks": overdue_tasks,
            "today_tasks": today_tasks,
            "dashboard_task_count": dashboard_task_count,
            "categories": categories,
        },
    )


@login_required(login_url="login")
def tasks_by_category(request, category_name):
    categories = models.Category.objects.filter(user=request.user)
    if category_name == "Inbox":
        tasks = models.Task.objects.filter(category=None, user=request.user)
    else:
        category = get_object_or_404(
            models.Category, name=category_name, user=request.user
        )
        tasks = models.Task.objects.filter(category=category, user=request.user)

    inbox_task_count = tasks.count()

    return render(
        request,
        "tasks_by_category.html",
        {
            "category_name": category_name,
            "tasks": tasks,
            "inbox_task_count": inbox_task_count,
            "categories": categories,
        },
    )


@login_required(login_url="login")
def create_task(request):
    if request.method == "POST":
        form = forms.TaskCreationForm(request.user, request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("dashboard")
    form = forms.TaskCreationForm(request.user)
    return render(request, "task_creation.html", {"form": form})


@login_required(login_url="login")
def create_category(request):
    if request.method == "POST":
        form = forms.CategoryCreationForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect("dashboard")
    form = forms.CategoryCreationForm()
    return render(request, "task_creation.html", {"form": form})
