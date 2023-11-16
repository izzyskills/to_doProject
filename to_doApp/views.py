from django.contrib.auth import authenticate
from rest_framework import viewsets, status, permissions, views
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Category, Task
from .serializers import (
    CategorySerializer,
    TaskSerializer,
    RegistrationSerializer,
    LoginSerializer,
)


class LoginView(views.APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data["username"].lower(),
            password=serializer.validated_data["password"],
        )
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )


class RegistrationView(views.APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DashboardViewSet(viewsets.ViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        today = timezone.now().date()
        overdue_tasks = Task.objects.filter(user=request.user, date__lt=today)
        today_tasks = Task.objects.filter(user=request.user, date=today)
        dashboard_task_count = today_tasks.count() + overdue_tasks.count()

        data = {
            "overdue_tasks": TaskSerializer(overdue_tasks, many=True).data,
            "today_tasks": TaskSerializer(today_tasks, many=True).data,
            "dashboard_task_count": dashboard_task_count,
            "categories": CategorySerializer(
                request.user.categories.all(), many=True
            ).data,
        }
        return Response(data, status=status.HTTP_200_OK)


class TasksByCategoryViewSet(viewsets.ViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, category_name=None):
        if category_name == "Inbox":
            tasks = Task.objects.filter(category=None, user=request.user)
        else:
            category = get_object_or_404(
                Category, name=category_name, user=request.user
            )
            tasks = Task.objects.filter(category=category, user=request.user)

        inbox_task_count = tasks.count()

        data = {
            "category_name": category_name,
            "tasks": self.serializer_class(tasks, many=True).data,
            "inbox_task_count": inbox_task_count,
            "categories": CategorySerializer(
                request.user.categories.all(), many=True
            ).data,
        }
        return Response(data, status=status.HTTP_200_OK)
