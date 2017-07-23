import sys
from django.core.management import BaseCommand

from visualization.models import Desk, Zone, Contestant


class Command(BaseCommand):
    help = 'Import desk contestant mapping'

    def split(self, line):
        return [x.strip() for x in line.split(',')]

    def handle(self, *args, **options):
        mapping = list(map(self.split, sys.stdin.readlines()))
        for contestant_code, desk_code in mapping:
            zone_name, desk_number = desk_code[0], int(desk_code[1:])
            country_code, contestant_number = contestant_code.split('-')
            desk = Desk.objects.get(zone=Zone.objects.get(name=zone_name), number=desk_number)
            contestant = Contestant.objects.get(number=contestant_number, team__country_code=country_code)
            desk.contestant = contestant
            desk.save()