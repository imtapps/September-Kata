from django.core.management.base import BaseCommand, CommandError

from bowling import models as bowling_models

class Command(BaseCommand):

    def handle(self, *args, **options):
        for scores in bowling_models.Scores.objects.all():
            print scores.score