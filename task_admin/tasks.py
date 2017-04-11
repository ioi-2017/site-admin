import datetime
import subprocess

import pytz

from paramiko import SSHClient, AutoAddPolicy

from netadmin.settings import app
from celery import Task

RUN_TIMEOUT_SECONDS = 10


class NetAdminTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        if retval['result']['return_code'] != 0:
            self.update_state(state='FAILED', meta=retval)


def add_time(f):
    def decorator(self, *args, **kwargs):
        start_time = datetime.datetime.now(pytz.timezone('Asia/Tehran'))
        self.update_state(state='PROGRESS', meta={'started_at': start_time.isoformat()})
        result = f(self, *args, **kwargs)
        finished_time = datetime.datetime.now(pytz.timezone('Asia/Tehran'))
        return {'result': result,
                'duration_milliseconds': int((finished_time - start_time).total_seconds() * 1000),
                'finished_at': finished_time.isoformat(),
                'started_at': start_time.isoformat(),
                }

    return decorator


@app.task(bind=True, base=NetAdminTask)
@add_time
def execute_task(self, is_local, ip, username, rendered_code):
    if is_local:
        try:
            command = subprocess.Popen((rendered_code,), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, universal_newlines=True)
            stdout, stderr = command.communicate(timeout=RUN_TIMEOUT_SECONDS)
            return {'stdout': str(stdout),
                    'stderr': str(stderr),
                    'return_code': command.returncode,
                    }
        except subprocess.TimeoutExpired as e:
            return {'stdout': '',
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
            return {'stdout': stdout.read().decode('utf-8'),
                    'stderr': stderr.read().decode('utf-8'),
                    'return_code': stdout.channel.recv_exit_status(),
                    }
        except Exception as e:
            return {'stdout': '',
                    'stderr': str(e),
                    'return_code': -1,
                    }
