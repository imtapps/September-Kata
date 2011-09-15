from django.core.management.base import BaseCommand
from django_bowling.bowling.game import main

class Command(BaseCommand):
    def handle(self, *args, **options):
        main()

