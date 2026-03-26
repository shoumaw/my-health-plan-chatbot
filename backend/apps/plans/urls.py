from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EnrollmentViewSet, PlanViewSet, SBCDocumentViewSet

router = DefaultRouter()
router.register(r"plans", PlanViewSet, basename="plan")
router.register(r"enrollments", EnrollmentViewSet, basename="enrollment")
router.register(r"sbc-documents", SBCDocumentViewSet, basename="sbcdocument")

urlpatterns = [
    path("v1/", include(router.urls)),
]
