import logging

import pdfplumber
from django.core.management.base import BaseCommand, CommandError

from api.models import SBCDocument

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        "Extract text from SBC PDF documents and store it in SBCDocument.extracted_text. "
        "By default, only processes documents with an empty extracted_text field."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--plan-id",
            type=str,
            help="Process only the SBCDocument belonging to this plan UUID.",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Re-extract text even if extracted_text is already populated.",
        )

    def handle(self, *args, **options):
        qs = SBCDocument.objects.select_related("plan").all()

        if options["plan_id"]:
            qs = qs.filter(plan__id=options["plan_id"])
            if not qs.exists():
                raise CommandError(f"No SBCDocument found for plan_id={options['plan_id']}")

        if not options["force"]:
            qs = qs.filter(extracted_text="")

        total = qs.count()
        if total == 0:
            self.stdout.write(self.style.WARNING("No documents to process."))
            return

        self.stdout.write(f"Processing {total} document(s)...")

        success = 0
        for doc in qs:
            try:
                text = self._extract_text(doc)
                doc.extracted_text = text
                doc.save(update_fields=["extracted_text", "updated_at"])
                self.stdout.write(
                    self.style.SUCCESS(f"  [{doc.plan.name}] extracted {len(text):,} chars")
                )
                success += 1
            except Exception as exc:
                self.stderr.write(
                    self.style.ERROR(f"  [{doc.plan.name}] failed: {exc}")
                )
                logger.exception("Failed to extract text for SBCDocument %s", doc.id)

        self.stdout.write(f"\nDone: {success}/{total} succeeded.")

    def _extract_text(self, doc: SBCDocument) -> str:
        pages = []
        with doc.file.open("rb") as f:
            with pdfplumber.open(f) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        pages.append(page_text)
        return "\n\n".join(pages)
