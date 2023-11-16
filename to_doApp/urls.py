from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r"tasks", views.TaskViewSet, basename="task")
router.register(r"category", views.CategoryViewSet, basename="category")
urlpatterns = [
    path("", include(router.urls)),
    path("register/", views.RegistrationView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
]
