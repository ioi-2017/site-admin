#!/bin/sh
celery -A task_admin.tasks worker --concurrency=2 -Q local_queue --loglevel=info &
celery -A task_admin.tasks worker --concurrency=10 -Q remote_queue --loglevel=info