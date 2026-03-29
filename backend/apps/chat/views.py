import logging

import groq
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ai_agent.service import get_ai_response
from apps.plans.models import Enrollment

logger = logging.getLogger(__name__)


@api_view(["GET"])
def health(request):
    return Response({"status": "ok"})


class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message = request.data.get("message", "").strip()
        history = request.data.get("history", [])

        if not message:
            return Response(
                {"error": "message is required", "code": "MISSING_MESSAGE"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not isinstance(history, list):
            history = []

        enrollments = (
            Enrollment.objects.filter(employee__user=request.user, is_active=True)
            .select_related("plan__sbc_document")
        )
        if not enrollments.exists():
            return Response(
                {"error": "No active plan enrollment found", "code": "NO_ENROLLMENT"},
                status=status.HTTP_404_NOT_FOUND,
            )

        enrolled_plans = []
        for enrollment in enrollments:
            plan = enrollment.plan
            sbc_text = None
            if hasattr(plan, "sbc_document") and plan.sbc_document.extracted_text:
                sbc_text = plan.sbc_document.extracted_text
            enrolled_plans.append({"name": plan.name, "sbc_text": sbc_text})

        try:
            ai_reply = get_ai_response(
                enrolled_plans=enrolled_plans,
                history=history,
                user_message=message,
            )
        except groq.APIError as exc:
            logger.exception("Groq API error: %s", exc)
            return Response(
                {"error": "AI service unavailable, please try again later", "code": "AI_ERROR"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response({"reply": ai_reply})
