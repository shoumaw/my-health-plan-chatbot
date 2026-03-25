import uuid
from django.db import models
from django.contrib.auth.models import User


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


class Plan(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    provider = models.CharField(max_length=255, blank=True)
    plan_year = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Plans"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Enrollment(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="enrollments")
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"
        ordering = ["-enrolled_at"]
        unique_together = [("employee", "plan")]

    def __str__(self):
        return f"{self.employee} → {self.plan}"


class SBCDocument(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan = models.OneToOneField(Plan, on_delete=models.CASCADE, related_name="sbc_document")
    file = models.FileField(upload_to="sbc_documents/")
    extracted_text = models.TextField(blank=True)

    class Meta:
        verbose_name = "SBC Document"
        verbose_name_plural = "SBC Documents"

    def __str__(self):
        return f"SBC — {self.plan.name}"

