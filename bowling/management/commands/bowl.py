from django.core.management import BaseCommand

from bowling import game

class Command(BaseCommand):

    def handle(self, *args, **options):
        game.main()