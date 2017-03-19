import datetime
import subprocess

import pytz
from dateutil.parser import parser

from celery import chord
from paramiko import SSHClient, AutoAddPolicy

from netadmin.settings import app

RUN_TIMEOUT_SECONDS = 10


@app.task
def execution_timer_task(previous_result=None, start_time_str=None):
    start_time = parser().parse(start_time_str)
    finished_time = datetime.datetime.now(pytz.timezone('Asia/Tehran'))
    finished_time_str = finished_time.isoformat()

    return {'result': previous_result,
            'duration_milliseconds': int((finished_time - start_time).total_seconds()*1000),
            'finished_at': finished_time_str,
            'started_at': start_time_str,
            }


def add_time(task):  # task shouldn't throw exceptions
    return chord(task, execution_timer_task.s(start_time_str=datetime.datetime.now(pytz.timezone('Asia/Tehran')).isoformat()))

@app.task
def execute_task(is_local, ip, username, rendered_code):
    if is_local:
        command = subprocess.Popen((rendered_code,), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = command.communicate(timeout=RUN_TIMEOUT_SECONDS)
        return {'stdout': str(stdout),
                'stderr': str(stderr),
                'return_code': command.returncode,
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
