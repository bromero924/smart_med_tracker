from django.core.management.base import BaseCommand
from django.utils import timezone
from medications.utils import process_dose_alerts


class Command(BaseCommand):
    help = "send medication dose alerts"

    def handle(self, *args, **kwargs):
        print(f"[{timezone.now()}] Processing dose alerts...")
        process_dose_alerts()
        print("DONE!")
