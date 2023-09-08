from django.db import models
from django.contrib.auth.models import User
import datetime
class Category(models.Model):
    name = models.CharField(max_length=20)
    user = models.ForeignKey(User,related_name="profile",on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.name
    

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User,related_name="profile",on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    date = models.DateField(default=datetime.date,null=True)
    status = models.BooleanField(default=False)
    overdue = models.BooleanField(default=False)