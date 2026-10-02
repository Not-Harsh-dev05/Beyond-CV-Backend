"""Train and save the versioned pedigree baseline model."""

from django.core.management.base import BaseCommand, CommandError
from apps.scoring.pedigree import train_model


class Command(BaseCommand):
    """Train a baseline on an operator-supplied CSV."""

    help = "Train the pedigree baseline from college_tier, employer_brand, competence columns."

    def add_arguments(self, parser):
        parser.add_argument("--data-path", required=True)

    def handle(self, *args, **options):
        try:
            output = train_model(options["data_path"])
        except (OSError, ValueError) as exc:
            raise CommandError(str(exc)) from exc
        self.stdout.write(
            self.style.SUCCESS(f"Saved versioned pedigree model to {output}")
        )
