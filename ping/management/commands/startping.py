import logging
import subprocess
import threading
import time
from django.core.management.base import BaseCommand
from django.db import DatabaseError

from ping.models import PingLog
from visualization.models import Node

logger = logging.getLogger(__name__)

DB_REFRESH_RATE = 60


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self._stop2 = threading.Event()

    def stop(self):
        self._stop2.set()

    def stopped(self):
        return self._stop2.isSet()


class Command(BaseCommand):
    help = 'Start the monitoring service'

    @staticmethod
    def extract_latency(ping_process):
        if ping_process.poll() == 0:
            return float(str(ping_process.communicate()[0]).split('/')[4])
        return 0

    @staticmethod
    def ping_node(node_ip, node_status, count):
        for idx in range(count):
            p = subprocess.Popen(['ping', '-c', '1', '-i', '0.2', node_ip], stdout=subprocess.PIPE)
            time.sleep(0.4)
            returncode = p.poll()
            if returncode is None:  # Ping not finished yet,
                p.kill()
                returncode = -1
            success = returncode == 0
            if node_status != success:
                node_status = success
                node = Node.objects.get(ip=node_ip)
                node.connected = success
                PingLog.objects.create(node=node, connected=success)
                node.save(update_fields=['connected'])
                if success:
                    logger.info('Node %s connected' % node.ip)
                else:
                    logger.info('Node %s disconnected' % node.ip)
            if threading.current_thread().stopped():
                from django.db import connections
                for conn in connections.all():
                    conn.close()
                return
            time.sleep(DB_REFRESH_RATE/count)

    def add_arguments(self, parser):
        parser.add_argument('pings_per_minute', type=int)

    def handle(self, *args, **options):
        count = options['pings_per_minute']

        while True:
            all_threads = []
            try:
                for node in Node.objects.all():
                    if node.ip is not None:
                        thread = StoppableThread(target=self.ping_node, args=(node.ip, node.connected, count))
                        thread.start()
                        all_threads.append(thread)
                time.sleep(DB_REFRESH_RATE)
                for thread in all_threads:
                    thread.stop()
                for thread in all_threads:
                    thread.join()
            except DatabaseError as e:
                print(e)
