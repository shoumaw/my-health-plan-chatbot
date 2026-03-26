from django.urls import path

from .views import ChatView, health

urlpatterns = [
    path("health/", health, name="health"),
    path("chat/", ChatView.as_view(), name="chat"),
]
