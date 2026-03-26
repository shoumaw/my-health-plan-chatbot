from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.select_related("user").all()
