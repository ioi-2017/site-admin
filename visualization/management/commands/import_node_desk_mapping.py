import sys
from django.core.management import BaseCommand

from visualization.models import Desk, Zone, Contestant, Node


class Command(BaseCommand):
    help = 'Import desk contestant mapping'

    def split(self, line):
        return [x.strip() for x in line.split(',')]

    def handle(self, *args, **options):
        mapping = list(map(self.split, sys.stdin.readlines()))
        for desk_code, node_id in mapping:
            zone_name, desk_number = desk_code[0], int(desk_code[1:])
            node_id = int(node_id)
            desk = Desk.objects.get(zone=Zone.objects.get(name=zone_name), number=desk_number)
            node = Node.objects.get(property_id=node_id)
            desk.active_node = node
            desk.save()