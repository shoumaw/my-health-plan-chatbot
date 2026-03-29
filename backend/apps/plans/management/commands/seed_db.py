import logging
import os
from datetime import date

import pdfplumber
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from apps.accounts.models import Employee
from apps.plans.models import Enrollment, Plan, SBCDocument

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "fixtures")
SAMPLE_SBC_PATH = os.path.join(FIXTURES_DIR, "sample-sbc.pdf")

logger = logging.getLogger(__name__)

# Hardcoded SBC text for Silver and Gold — distinct values from Bronze Essential
PLAN_SBC_OVERRIDES = {
    "Silver Select": """Summary of Benefits and Coverage: What this Plan Covers & What You Pay for Covered Services
Coverage Period: 01/01/2026 – 12/31/2026
Silver Select | Provider: Aetna | Plan Type: PPO | Coverage for: Individual + Family

Important Questions | Answers | Why This Matters
What is the overall deductible? | $2,500 / individual or $5,000 / family | You must meet this deductible before the plan pays for most services.
Are there services covered before you meet your deductible? | Yes. Preventive care and primary care visits are covered before the deductible. | You can get preventive and primary care without meeting the deductible first.
Are there other deductibles for specific services? | $150 for prescription drugs. No other specific deductibles. | You must pay up to $150 for prescriptions before drug coverage kicks in.
What is the out-of-pocket limit? | $4,500 individual / $9,000 family (in-network); $7,000 individual / $14,000 family (out-of-network) | This is the most you will pay in a plan year for covered services.
What is not included in the out-of-pocket limit? | Premiums, balance-billing charges, and non-covered services. | These costs do not count toward your out-of-pocket limit.

Common Medical Events | In-Network Cost | Out-of-Network Cost
Primary care visit | $25 copay | 40% coinsurance after deductible
Specialist visit | $50 copay | 40% coinsurance after deductible
Preventive care | No charge | 40% coinsurance
Emergency room care | $200 copay | $200 copay (waived if admitted)
Urgent care | $50 copay | $75 copay
Hospital stay (facility) | 20% coinsurance after deductible | 40% coinsurance after deductible
Mental health outpatient | $25 copay | 40% coinsurance after deductible
Generic drugs (Tier 1) | $10 copay | $30 copay
Preferred brand drugs (Tier 2) | $45 copay | $90 copay
Non-preferred brand drugs (Tier 3) | $80 copay | $160 copay
Specialty drugs (Tier 4) | 25% coinsurance | 50% coinsurance
Lab work | $30 copay | 40% coinsurance after deductible
Imaging (X-ray, MRI, CT) | $75 copay | 40% coinsurance after deductible
Outpatient surgery | 20% coinsurance after deductible | 40% coinsurance after deductible

This plan includes coverage for dental exams (1 per year, $0 copay in-network) and vision exams (1 per year, $20 copay).
For questions contact Aetna Member Services at 1-800-555-2000 or visit www.aetna.com.
""",

    "Gold Premium Care": """Summary of Benefits and Coverage: What this Plan Covers & What You Pay for Covered Services
Coverage Period: 01/01/2026 – 12/31/2026
Gold Premium Care | Provider: UnitedHealthcare | Plan Type: PPO | Coverage for: Individual + Family

Important Questions | Answers | Why This Matters
What is the overall deductible? | $500 / individual or $1,000 / family | Very low deductible — the plan starts paying quickly after a small upfront cost.
Are there services covered before you meet your deductible? | Yes. Preventive care, primary care, specialist visits, and mental health are covered before the deductible. | You have broad access to care before needing to meet the deductible.
Are there other deductibles for specific services? | None. | No additional deductibles apply to any specific services.
What is the out-of-pocket limit? | $2,500 individual / $5,000 family (in-network); $5,000 individual / $10,000 family (out-of-network) | The lowest out-of-pocket cap across all available plans.
What is not included in the out-of-pocket limit? | Premiums and balance-billing charges. | These do not count toward your annual maximum.

Common Medical Events | In-Network Cost | Out-of-Network Cost
Primary care visit | $10 copay | 30% coinsurance after deductible
Specialist visit | $30 copay | 30% coinsurance after deductible
Preventive care | No charge | 30% coinsurance
Emergency room care | $100 copay | $100 copay (waived if admitted)
Urgent care | $25 copay | $40 copay
Hospital stay (facility) | 10% coinsurance after deductible | 30% coinsurance after deductible
Mental health outpatient | $10 copay | 30% coinsurance after deductible
Generic drugs (Tier 1) | $5 copay | $20 copay
Preferred brand drugs (Tier 2) | $25 copay | $60 copay
Non-preferred brand drugs (Tier 3) | $55 copay | $110 copay
Specialty drugs (Tier 4) | 15% coinsurance | 40% coinsurance
Lab work | $15 copay | 30% coinsurance after deductible
Imaging (X-ray, MRI, CT) | $40 copay | 30% coinsurance after deductible
Outpatient surgery | 10% coinsurance after deductible | 30% coinsurance after deductible

This plan includes comprehensive dental (exams, cleanings, and fillings covered at 100% in-network),
vision (frames or contacts up to $200/year), maternity care, and broad specialist network access.
For questions contact UnitedHealthcare at 1-800-555-3000 or visit www.uhc.com.
""",
}

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
        employee = self._seed_mock_user()
        self._seed_plans()
        self._seed_sbc_documents()
        if employee:
            self._seed_enrollments(employee)

    def _seed_mock_user(self):
        email = os.environ.get("MOCK_USER_EMAIL", "").strip()
        if not email:
            return None

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

        employee, _ = Employee.objects.get_or_create(
            user=user,
            defaults={"employee_id": "EMP-001", "department": "Engineering"},
        )
        return employee

    def _seed_plans(self):
        for data in PLANS:
            _, created = Plan.objects.get_or_create(name=data["name"], defaults=data)
            if created:
                logger.info("seed_db: created plan '%s'", data["name"])

    def _seed_sbc_documents(self):
        """Attach SBC documents to all plans. Bronze uses the real PDF; Silver and Gold use hardcoded text."""
        bronze_extracted = None
        pdf_bytes = None

        if os.path.exists(SAMPLE_SBC_PATH):
            pages = []
            with pdfplumber.open(SAMPLE_SBC_PATH) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        pages.append(page_text)
            bronze_extracted = "\n\n".join(pages)
            with open(SAMPLE_SBC_PATH, "rb") as f:
                pdf_bytes = f.read()
        else:
            logger.warning("seed_db: sample SBC PDF not found at %s", SAMPLE_SBC_PATH)

        for plan in Plan.objects.all():
            if hasattr(plan, "sbc_document") and plan.sbc_document.extracted_text:
                logger.info("seed_db: SBC for '%s' already exists — skipping", plan.name)
                continue

            override_text = PLAN_SBC_OVERRIDES.get(plan.name)
            extracted_text = override_text or bronze_extracted

            if not extracted_text:
                logger.warning("seed_db: no SBC text available for '%s' — skipping", plan.name)
                continue

            slug = plan.name.lower().replace(" ", "-")
            filename = f"{slug}-sbc.pdf"
            file_content = ContentFile(pdf_bytes or extracted_text.encode())

            if hasattr(plan, "sbc_document"):
                doc = plan.sbc_document
                doc.file.save(filename, file_content, save=False)
                doc.extracted_text = extracted_text
                doc.save(update_fields=["file", "extracted_text", "updated_at"])
            else:
                doc = SBCDocument(plan=plan, extracted_text=extracted_text)
                doc.file.save(filename, file_content, save=False)
                doc.save()

            logger.info("seed_db: seeded SBC for '%s' (%d chars)", plan.name, len(extracted_text))

    def _seed_enrollments(self, employee):
        """Enroll the mock employee in all plans."""
        for plan in Plan.objects.all():
            _, created = Enrollment.objects.get_or_create(
                employee=employee,
                plan=plan,
                defaults={"enrolled_at": date.today(), "is_active": True},
            )
            if created:
                logger.info("seed_db: enrolled %s in '%s'", employee, plan.name)
