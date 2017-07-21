import os
import sys

NETADMIN_BROKER_IP = os.environ.get('NETADMIN_BROKER', 'localhost')
NETADMIN_BROKER_PORT = int(os.environ.get('NETADMIN_BROKER_PORT', '6379'))

result_backend = 'db+sqlite:///celery-results.sqlite'
broker_url = 'redis://%s:%d/0' % (NETADMIN_BROKER_IP, NETADMIN_BROKER_PORT)
task_track_started = True

if sys.argv[1:2] == ['test']:
    broker_url = 'memory'
    task_always_eager = True
    task_eager_propagates = True
