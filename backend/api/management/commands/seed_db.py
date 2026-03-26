import logging
import os

import pdfplumber
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from api.models import Employee, Plan, SBCDocument

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "fixtures")
SAMPLE_SBC_PATH = os.path.join(FIXTURES_DIR, "sample-sbc.pdf")

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
        self._seed_sbc_document()

    def _seed_mock_user(self):
        import os

        email = os.environ.get("MOCK_USER_EMAIL", "").strip()
        if not email:
            return

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": email.split("@")[0],
                "first_name": "Dan",
                "last_name": "Smith",
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

    def _seed_sbc_document(self):
        """Attach the sample SBC PDF to the Bronze Essential plan and extract its text."""
        if not os.path.exists(SAMPLE_SBC_PATH):
            logger.warning("seed_db: sample SBC PDF not found at %s — skipping", SAMPLE_SBC_PATH)
            return

        try:
            plan = Plan.objects.get(name="Bronze Essential")
        except Plan.DoesNotExist:
            logger.warning("seed_db: Bronze Essential plan not found — skipping SBC seed")
            return

        # Skip if a doc already exists with extracted text
        if hasattr(plan, "sbc_document") and plan.sbc_document.extracted_text:
            logger.info("seed_db: SBC document for Bronze Essential already extracted — skipping")
            return

        pages = []
        with pdfplumber.open(SAMPLE_SBC_PATH) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    pages.append(page_text)
        extracted_text = "\n\n".join(pages)

        with open(SAMPLE_SBC_PATH, "rb") as f:
            pdf_bytes = f.read()

        if hasattr(plan, "sbc_document"):
            doc = plan.sbc_document
            doc.file.save("bronze-essential-sbc.pdf", ContentFile(pdf_bytes), save=False)
            doc.extracted_text = extracted_text
            doc.save(update_fields=["file", "extracted_text", "updated_at"])
            logger.info("seed_db: updated SBC document for Bronze Essential (%d chars)", len(extracted_text))
        else:
            doc = SBCDocument(plan=plan, extracted_text=extracted_text)
            doc.file.save("bronze-essential-sbc.pdf", ContentFile(pdf_bytes), save=False)
            doc.save()
            logger.info("seed_db: created SBC document for Bronze Essential (%d chars)", len(extracted_text))
