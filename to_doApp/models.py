from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20)
    user = models.ForeignKey(User, related_name="owner", on_delete=models.CASCADE)

    def clean(self):
        if " " in self.name:
            raise ValidationError("Category names cannot contain spaces.")

    def save(self, *args, **kwargs):
        self.clean()
        super(Category, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    user = models.ForeignKey(User, related_name="profile", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    date = models.DateField(blank=True, null=True)
    status = models.BooleanField(default=False)
    recurrence = models.IntegerField(
        choices=[(0, "none"), (1, "daily"), (2, "Weekly"), (3, "Monthly")]
    )

    def save(self, *args, **kwargs):
        if self.date is None and self.recurrence != 0:
            self.date = datetime.date.today()
        if self.pk and self.status and self.recurrence != 0:
            if self.recurrence == 1:
                self.date += datetime.timedelta(days=1)
            elif self.recurrence == 2:
                self.date += datetime.timedelta(weeks=1)
            elif self.recurrence == 3:
                self.date = self.date.replace(day=1) + datetime.timedelta(days=30)

            self.status = False

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name} :{self.user}"
