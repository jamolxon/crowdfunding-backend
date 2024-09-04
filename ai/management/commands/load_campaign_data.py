from django.core.management import BaseCommand
from django.db import transaction
from ai.utils import load_campaign_data, load_interaction_data


class Command(BaseCommand):
    help = "Cron testing"

    def handle(self, *args, **options):

        with transaction.atomic():
            load_campaign_data()
            load_interaction_data()
        self.stdout.write(
            self.style.SUCCESS("Successfully imported campaigns and interactions.")
        )
