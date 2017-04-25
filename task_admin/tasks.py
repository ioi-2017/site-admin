import datetime
import os
import subprocess

import django
import pytz
from celery import Task
from paramiko import SSHClient, AutoAddPolicy

from netadmin.settings import app

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "netadmin.settings")
django.setup()

from task_admin.models import TaskRun

RUN_TIMEOUT_SECONDS = 10


@app.task
def execute_task(task_run_id, is_local, ip, username, rendered_code):
    task_run = TaskRun.objects.get(id=task_run_id)
    task_run.status = 'PROGRESS'
    task_run.started_at = datetime.datetime.now()
    task_run.save()
    if is_local:
        try:
            command = subprocess.Popen((rendered_code,), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, universal_newlines=True)
            stdout, stderr = command.communicate(timeout=RUN_TIMEOUT_SECONDS)
            result = {'stdout': str(stdout),
                      'stderr': str(stderr),
                      'return_code': command.returncode,
                      }
        except subprocess.TimeoutExpired as e:
            result = {'stdout': '',
                      'stderr': str(e),
                      'return_code': -1,
                      }

    else:
        try:
            client = SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(ip, username=username, timeout=RUN_TIMEOUT_SECONDS)
            stdin, stdout, stderr = client.exec_command(rendered_code)
            result = {'stdout': stdout.read().decode('utf-8'),
                      'stderr': stderr.read().decode('utf-8'),
                      'result =_code': stdout.channel.recv_exit_status(),
                      }
        except Exception as e:
            result = {'stdout': '',
                      'stderr': str(e),
                      'return_code': -1,
                      }
    task_run.finished_at = datetime.datetime.now()
    task_run.stdout = result['stdout']
    task_run.stderr = result['stderr']
    task_run.return_code = result['return_code']
    if result['return_code'] != 0:
        task_run.status = 'FAILURE'
    else:
        task_run.status = 'SUCCESS'
    task_run.save()
