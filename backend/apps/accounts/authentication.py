import os

from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class MockEmployeeAuthentication(BaseAuthentication):
    """
    Development-only authenticator.
    Reads MOCK_USER_EMAIL from the environment and returns that user
    as the authenticated identity — no token required.

    This class is a no-op when DEBUG is False, so it can never
    accidentally grant access in production.
    """

    def authenticate(self, request):
        from django.conf import settings

        if not settings.DEBUG:
            return None

        email = os.environ.get("MOCK_USER_EMAIL", "").strip()
        if not email:
            return None

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed(
                f"MOCK_USER_EMAIL '{email}' does not match any user in the database."
            )

        return (user, None)
