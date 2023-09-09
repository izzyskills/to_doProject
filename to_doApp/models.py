from django.db import models
from django.contrib.auth.models import User
import datetime
    

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20)
    user = models.ForeignKey(User,related_name="profile",on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.name
class Task(models.Model):
    user = models.ForeignKey(User,related_name="profile",on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100,blank=True,null=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)
    date = models.DateField(blank=True,null=True)
    status = models.BooleanField(default=False)
    overdue = models.BooleanField(default=False)
    recurrence = models.CharField(max_length=50, null=True, blank=True)