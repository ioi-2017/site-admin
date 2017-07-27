import sys
from django.core.management import BaseCommand

from visualization.models import Desk, Zone, Contestant, Node


class Command(BaseCommand):
    help = 'Import desk contestant mapping'

    def split(self, line):
        return [x.strip() for x in line.split('\t')]

    def handle(self, *args, **options):
        dhcp_data = list(map(self.split, sys.stdin.readlines()[1:]))
        for line in dhcp_data:
            ip, _, _, _, mac, _, _, _, _, _ = line
            mac_address = ':'.join([mac[0:2], mac[2:4], mac[4:6], mac[6:8], mac[8:10], mac[10:12]]).upper()
            try:
                node = Node.objects.get(mac_address=mac_address)
                if node.ip != ip:
                    print('Changed', node.ip, ip)
                node.ip = ip
                node.save()
            except Exception:
                print('Mac address %s not found.' % mac_address)
