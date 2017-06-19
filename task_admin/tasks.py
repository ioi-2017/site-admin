import datetime
import os
import stat
import subprocess
import tempfile
import django
from paramiko import SSHClient, AutoAddPolicy
from netadmin.settings import app

TIMEOUT_EXIT_CODE = 124

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "netadmin.settings")
django.setup()

from task_admin.models import TaskRun

SSH_CONNECTION_TIMEOUT = 1


@app.task
def execute_task(task_run_id, is_local, ip, username, rendered_code, timeout):
    task_run = TaskRun.objects.get(id=task_run_id)
    task_run.change_status('PROGRESS', commit=False)
    task_run.started_at = datetime.datetime.now()
    task_run.save(update_fields=['status', 'started_at'])

    # Prepare the script
    script = tempfile.NamedTemporaryFile('w', delete=False)
    script.write(rendered_code)
    script.close()
    st = os.stat(script.name)
    os.chmod(script.name, st.st_mode | stat.S_IEXEC)

    if is_local:
        process = subprocess.Popen(('timeout', str(timeout), script.name,),
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = process.communicate()
        result = {'stdout': str(stdout),
                  'stderr': 'Execution timeout' if process.returncode == TIMEOUT_EXIT_CODE else str(stderr),
                  'return_code': process.returncode,
                  }


    else:
        try:
            client = SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(ip, username=username, timeout=SSH_CONNECTION_TIMEOUT)
            sftp = client.open_sftp()
            script_remote_path = '/tmp/.taskrun%d.sh' % task_run_id
            sftp.put(script.name, script_remote_path)
            stdin, stdout, stderr = client.exec_command('chmod +x %s' % script_remote_path)
            exit_status = stdout.channel.recv_exit_status()
            assert (exit_status == 0)
            stdin, stdout, stderr = client.exec_command('bash -lc "timeout %s %s"' % (timeout, script_remote_path),
                                                        timeout=SSH_CONNECTION_TIMEOUT)
            result = {'stdout': stdout.read().decode('utf-8'),
                      'stderr': stderr.read().decode('utf-8'),
                      'return_code': stdout.channel.recv_exit_status(),
                      }
            sftp.remove(script_remote_path)
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
        task_run.change_status('FAILURE')
    else:
        task_run.change_status('SUCCESS')
    task_run.save(update_fields=['status', 'finished_at', 'stdout', 'stderr', 'return_code'])

    os.remove(script.name)
