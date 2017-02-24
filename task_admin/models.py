import subprocess

from celery.result import AsyncResult
from django.contrib.auth.models import User
from django.db import models
from paramiko import SSHClient, AutoAddPolicy

from visualization.models import Desk, Node, Contestant

RUN_TIMEOUT_SECONDS = 10


class Task(models.Model):
    is_local = models.BooleanField()
    name = models.CharField(max_length=100)
    code = models.TextField()
    author = models.ForeignKey(User)
    created_at = models.DateTimeField()
    deleted = models.BooleanField()

    def __str__(self):
        return '[%s] by %s' % (self.name, self.author)


class TaskRunSet(models.Model):
    task = models.ForeignKey(Task)
    created_at = models.DateTimeField(auto_created=True)

    @property
    def finished_at(self):
        # finished_at = 0
        # for task_run in self.taskrun_set.all():
        #     finished_at = max(finished_at, task_run.finished_at)
        # return finished_at
        raise NotImplemented()


class TaskRun(models.Model):
    celery_task = models.CharField(max_length=255, unique=True)
    is_local = models.BooleanField()
    run_set = models.ForeignKey(TaskRunSet)
    created_at = models.DateTimeField(auto_created=True)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField()
    rendered_code = models.TextField()

    desk = models.ForeignKey(Desk)
    contestant = models.ForeignKey(Contestant)
    node = models.ForeignKey(Node)

    def run(self):
        if self.is_local:
            client = SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(self.node.ip, username=self.node.username, timeout=RUN_TIMEOUT_SECONDS)
            stdin, stdout, stderr = client.exec_command(self.rendered_code)
            return stdout.read()
        else:
            command = subprocess.Popen((self.rendered_code,), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            return command.communicate(timeout=RUN_TIMEOUT_SECONDS)

    def get_celery_result(self):
        return AsyncResult(self.celery_task)

    @property
    def is_successful(self):
        return self.get_celery_result().successful()

    @property
    def duration(self):
        raise NotImplemented()

    @property
    def started_at(self):
        raise NotImplemented()

    @property
    def created_at(self):
        raise NotImplemented()

    @property
    def finished_at(self):
        raise NotImplemented()
