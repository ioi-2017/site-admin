import subprocess
import threading
import time

from django.core.management.base import BaseCommand

from visualization.models import Node

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

    def ping_node(self, node):
        from django.utils.termcolors import colorize
        self.stdout.write(colorize('started pinging {0:s}'.format(node.ip), fg="blue"))
        while True:
            p = subprocess.Popen(['ping', '-c', '1', "-W", "1", node.ip], stdout=subprocess.PIPE)
            p.wait()
            if p.poll():
                self.stdout.write(self.style.ERROR('ping {0:s} failed'.format(node.ip)))
                # do some shit
            if threading.current_thread().stopped():
                # self.stdout.write(self.style.NOTICE('finished pinging {0:s}'.format(node.ip)))
                return
            time.sleep(1)

    def handle(self, *args, **options):
        while True:
            all_threads = []
            for node in Node.objects.all():
                thread = StoppableThread(target=self.ping_node, args=(node,))
                thread.start()
                all_threads.append(thread)
            time.sleep(DB_REFRESH_RATE)
            for thread in all_threads:
                thread.stop()
            for thread in all_threads:
                thread.join()
