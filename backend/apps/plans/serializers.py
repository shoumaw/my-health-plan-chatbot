from rest_framework import serializers

from .models import Enrollment, Plan, SBCDocument


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ["id", "name", "description", "provider", "plan_year", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


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
