import logging

import groq
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ai_agent.service import get_ai_response
from .models import Employee, Plan, Enrollment, SBCDocument

logger = logging.getLogger(__name__)
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


class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message = request.data.get("message", "").strip()
        plan_id = request.data.get("plan_id", "").strip()

        if not message:
            return Response(
                {"error": "message is required", "code": "MISSING_MESSAGE"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not plan_id:
            return Response(
                {"error": "plan_id is required", "code": "MISSING_PLAN_ID"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            plan = Plan.objects.select_related("sbc_document").get(pk=plan_id)
        except Plan.DoesNotExist:
            return Response(
                {"error": "Plan not found", "code": "PLAN_NOT_FOUND"},
                status=status.HTTP_404_NOT_FOUND,
            )

        sbc_text = None
        if hasattr(plan, "sbc_document") and plan.sbc_document.extracted_text:
            sbc_text = plan.sbc_document.extracted_text

        try:
            ai_reply = get_ai_response(
                plan_name=plan.name,
                sbc_text=sbc_text,
                user_message=message,
            )
        except groq.APIError as exc:
            logger.exception("Groq API error: %s", exc)
            return Response(
                {"error": "AI service unavailable, please try again later", "code": "AI_ERROR"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response({"reply": ai_reply})
