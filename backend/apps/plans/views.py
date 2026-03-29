from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Enrollment, Plan, SBCDocument
from .serializers import (
    EnrollmentSerializer,
    PlanSerializer,
    SBCDocumentSerializer,
    SBCDocumentWriteSerializer,
)


class PlanViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PlanSerializer

    def get_queryset(self):
        return Plan.objects.filter(
            enrollments__employee__user=self.request.user,
            enrollments__is_active=True,
        )


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
