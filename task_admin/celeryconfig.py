import sys

result_backend = 'db+sqlite:///celery-results.sqlite'
broker_url = 'redis://localhost:6379/0'
task_track_started = True

if sys.argv[1:2] == ['test']:
    broker_url = 'memory'
    task_always_eager = True
    task_eager_propagates = True
