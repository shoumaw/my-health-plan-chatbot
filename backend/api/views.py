from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Employee, Plan, Enrollment, SBCDocument
from .serializers import (
    EmployeeSerializer,
    PlanSerializer,
    EnrollmentSerializer,
    SBCDocumentSerializer,
    SBCDocumentWriteSerializer,
)


@api_view(['GET'])
def health(request):
    return Response({'status': 'ok'})


class EmployeeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.select_related("user").all()


class PlanViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()


class EnrollmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EnrollmentSerializer
    queryset = Enrollment.objects.select_related("employee__user", "plan").all()


class SBCDocumentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = SBCDocument.objects.select_related("plan").all()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return SBCDocumentWriteSerializer
        return SBCDocumentSerializer
