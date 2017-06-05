import datetime
import os
import subprocess

import django
from paramiko import SSHClient, AutoAddPolicy

from netadmin.settings import app

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "netadmin.settings")
django.setup()

from task_admin.models import TaskRun

SSH_CONNECTION_TIMEOUT = 1


@app.task
def execute_task(task_run_id, is_local, ip, username, rendered_code, timeout):
    task_run = TaskRun.objects.get(id=task_run_id)
    task_run.status = 'PROGRESS'
    task_run.started_at = datetime.datetime.now()
    task_run.save(update_fields=['status', 'started_at'])
    if is_local:
        try:
            command = subprocess.Popen((rendered_code,), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, universal_newlines=True)
            stdout, stderr = command.communicate(timeout=timeout)
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
            client.connect(ip, username=username, timeout=SSH_CONNECTION_TIMEOUT)
            stdin, stdout, stderr = client.exec_command(rendered_code, timeout=timeout)
            result = {'stdout': stdout.read().decode('utf-8'),
                      'stderr': stderr.read().decode('utf-8'),
                      'return_code': stdout.channel.recv_exit_status(),
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
    task_run.save(update_fields=['status', 'finished_at', 'stdout', 'stderr', 'return_code'])
