from rest_framework import serializers

from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ["id", "user", "employee_id", "department", "full_name", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_full_name(self, obj):
        return obj.user.get_full_name()
