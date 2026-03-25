import logging

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from api.models import Employee, Plan

logger = logging.getLogger(__name__)

PLANS = [
    {
        "name": "Bronze Essential",
        "description": (
            "An affordable plan with core coverage for preventive care, emergency "
            "services, and prescription drugs. Best for healthy individuals who want "
            "protection against unexpected costs."
        ),
        "provider": "BlueCross BlueShield",
        "plan_year": 2026,
    },
    {
        "name": "Silver Select",
        "description": (
            "A balanced plan offering moderate premiums with solid coverage for primary "
            "care, specialist visits, mental health services, and hospitalizations."
        ),
        "provider": "Aetna",
        "plan_year": 2026,
    },
    {
        "name": "Gold Premium Care",
        "description": (
            "Comprehensive coverage with low deductibles and co-pays. Includes dental, "
            "vision, mental health, maternity, and broad specialist network access."
        ),
        "provider": "UnitedHealthcare",
        "plan_year": 2026,
    },
]


class Command(BaseCommand):
    help = "Seed the database with a mock employee and sample health plans (idempotent)."

    def handle(self, *args, **options):
        self._seed_mock_user()
        self._seed_plans()

    def _seed_mock_user(self):
        import os

        email = os.environ.get("MOCK_USER_EMAIL", "").strip()
        if not email:
            return

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": email.split("@")[0],
                "first_name": "Alex",
                "last_name": "Johnson",
            },
        )
        if created:
            user.set_password("unused")
            user.save()
            logger.info("seed_db: created user %s", email)

        Employee.objects.get_or_create(
            user=user,
            defaults={"employee_id": "EMP-001", "department": "Engineering"},
        )

    def _seed_plans(self):
        for data in PLANS:
            _, created = Plan.objects.get_or_create(name=data["name"], defaults=data)
            if created:
                logger.info("seed_db: created plan '%s'", data["name"])
