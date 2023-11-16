from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Category
from django.conf import settings
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def create_default_categories(sender, instance, created, **kwargs):
    if created:
        default_categories = ["Home", "Education", "Work"]
        for category_name in default_categories:
            Category.objects.create(name=category_name, user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
