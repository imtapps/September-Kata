from django.core.management import BaseCommand

from bowling import models

class Command(BaseCommand):

    def handle(self, *args, **options):
        bowler = args[0]
        for score in models.BowlingScore.get_by_name(bowler):
            print score.score

