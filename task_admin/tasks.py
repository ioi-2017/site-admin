from celery import Celery
from paramiko import SSHClient, AutoAddPolicy
import subprocess

RUN_TIMEOUT_SECONDS = 10

app = Celery('tasks', broker='redis://localhost:6379/0',backend='redis://localhost:6379/0')


@app.task
def execute_task(is_local, ip, username, rendered_code):
    if is_local:
        command = subprocess.Popen((rendered_code,), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        return command.communicate(timeout=RUN_TIMEOUT_SECONDS)
    else:
        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(ip, username=username, timeout=RUN_TIMEOUT_SECONDS)
        stdin, stdout, stderr = client.exec_command(rendered_code)
        return stdout.read().decode('utf-8')
