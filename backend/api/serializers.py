from rest_framework import serializers
from .models import Employee, Plan, Enrollment, SBCDocument


# ---------------------------------------------------------------------------
# Employee
# ---------------------------------------------------------------------------

class EmployeeSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ["id", "user", "employee_id", "department", "full_name", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_full_name(self, obj):
        return obj.user.get_full_name()


# ---------------------------------------------------------------------------
# Plan
# ---------------------------------------------------------------------------

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ["id", "name", "description", "provider", "plan_year", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


# ---------------------------------------------------------------------------
# Enrollment
# ---------------------------------------------------------------------------

class EnrollmentSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    plan_name = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = [
            "id", "employee", "employee_name", "plan", "plan_name",
            "enrolled_at", "is_active", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_employee_name(self, obj):
        return str(obj.employee)

    def get_plan_name(self, obj):
        return str(obj.plan)


# ---------------------------------------------------------------------------
# SBCDocument
# ---------------------------------------------------------------------------

class SBCDocumentSerializer(serializers.ModelSerializer):
    plan_name = serializers.SerializerMethodField()

    class Meta:
        model = SBCDocument
        fields = ["id", "plan", "plan_name", "file", "extracted_text", "created_at", "updated_at"]
        read_only_fields = ["id", "extracted_text", "created_at", "updated_at"]

    def get_plan_name(self, obj):
        return str(obj.plan)


class SBCDocumentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SBCDocument
        fields = ["id", "plan", "file"]
        read_only_fields = ["id"]
