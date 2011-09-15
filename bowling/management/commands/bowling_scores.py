from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, name, *args, **options):
        print name + ": [20][39][48][56][64][70][78][98][128][158]"
        print name + ": [30][53][71][79][94][104][112][120][134][154]"
        print name + ": [30][60][90][120][150][180][210][240][270][300]"