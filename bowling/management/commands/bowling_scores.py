from django.core.management.base import BaseCommand
from bowling.models import BowlingModel

class Command(BaseCommand):
    def handle(self, name, *args, **options):
        for entry in BowlingModel.objects.filter(name=name):
            print entry.name + ": " + entry.score
