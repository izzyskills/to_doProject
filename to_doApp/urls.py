from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logoutUser, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("create/task/", views.create_task, name="create_task"),
    path("create/category/", views.create_category, name="create_category"),
    path(
        "category/<slug:category_name>/",
        views.tasks_by_category,
        name="tasks_by_category",
    ),
]
