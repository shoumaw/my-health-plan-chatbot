from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'employees', views.EmployeeViewSet, basename='employee')
router.register(r'plans', views.PlanViewSet, basename='plan')
router.register(r'enrollments', views.EnrollmentViewSet, basename='enrollment')
router.register(r'sbc-documents', views.SBCDocumentViewSet, basename='sbcdocument')

urlpatterns = [
    path('health/', views.health, name='health'),
    path('chat/', views.ChatView.as_view(), name='chat'),
    path('v1/', include(router.urls)),
]
