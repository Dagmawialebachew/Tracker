from django.core.management.base import BaseCommand
from tracker.models import Laborer, Attendance
from django.utils import timezone

class Command(BaseCommand):
    help = "Resets all laborers' attendance to Absent at the start of the day"

    def handle(self, *args, **kwargs):
        today = timezone.localdate()
        laborers = Laborer.objects.all()
        for laborer in laborers:
            # Only create if today's attendance doesn't exist
            attendance, created = Attendance.objects.get_or_create(
                laborer=laborer,
                project=laborer.assigned_project,
                date=today,
                defaults={'status': 'Absent'}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Attendance created for {laborer.name}'))
            else:
                self.stdout.write(f'Attendance already exists for {laborer.name}')
