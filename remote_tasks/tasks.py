from celery import Celery
from paramiko import SSHClient, AutoAddPolicy

app = Celery('tasks', broker='redis://192.168.99.100:6379/0', backend='redis://192.168.99.100:6379/0')


@app.task
def run_ssh(node_ip, command):
    client = SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(node_ip)
    stdin, stdout, stderr = client.exec_command(command)
    return stdin, stdout, stderr
