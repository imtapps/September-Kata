from django.core.management.base import BaseCommand, CommandError

from bowling import game
from bowling import models as bowling_models

class Command(BaseCommand):

    def handle(self, *args, **options):
        lane = game.BowlingLane()
        lane.prompt_for_bowlers()
        lane.play_game()
        for player_game in lane.formatted_scores:
            bowling_models.Scores.objects.create(score=player_game)
            print player_game