from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from to_doApp import models


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        validated_data["username"] = validated_data["username"].lower()
        return User.objects.create_user(**validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ["id", "name"]

    def validate_name(self, value):
        # Check if name contains spaces
        if " " in value:
            raise ValidationError("Category names cannot contain spaces.")
        return value


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = [
            "id",
            "name",
            "description",
            "category",
            "date",
            "recurrence",
            "status",
        ]
