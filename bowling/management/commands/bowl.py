from django.core.management.base import BaseCommand, CommandError

from bowling import game

class Command(BaseCommand):

    def handle(self, *args, **options):
        lane = game.BowlingLane()
        lane.prompt_for_bowlers()
        lane.play_game()
        #lane.display_results()