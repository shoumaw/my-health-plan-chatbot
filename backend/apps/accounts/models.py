import uuid

from django.contrib.auth.models import User
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Employee(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee_profile")
    employee_id = models.CharField(max_length=50, unique=True, blank=True)
    department = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        ordering = ["user__last_name", "user__first_name"]

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.email})"
