import textwrap
from collections import Counter

from celery.result import AsyncResult
from dateutil.parser import parser
from django.contrib.auth.models import User
from django.db import models

from visualization.models import Desk, Node, Contestant


class Task(models.Model):
    is_local = models.BooleanField()
    name = models.CharField(max_length=100)
    code = models.TextField()
    author = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return '[%s] by %s' % (self.name, self.author)


class TaskRunSet(models.Model):
    name = models.TextField(blank=True)
    is_local = models.BooleanField()
    code = models.TextField()
    owner = models.ForeignKey(User, related_name='taskrunset', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    @property
    def last_finished_at(self):
        return max(task_run.finished_at for task_run in self.taskruns.all())

    @property
    def max_duration_milliseconds(self):
        return max(task_run.duration_milliseconds for task_run in self.taskruns.all())

    @property
    def summary(self):
        counter = Counter([task_run.status for task_run in self.taskruns.all()])
        return counter

    @property
    def is_finished(self):
        return self.summary.get('PENDING', 0) == 0

    @property
    def results(self):
        return [task_run.status for task_run in self.taskruns.all()]

    def number_of_nodes(self):
        return self.taskruns.count()

    def __str__(self):
        return '[%s] on %d nodes' % (textwrap.shorten(self.code, 20), self.number_of_nodes())


class TaskRun(models.Model):
    celery_task = models.CharField(max_length=255, unique=True, null=True)
    is_local = models.BooleanField()
    run_set = models.ForeignKey(TaskRunSet, related_name='taskruns')
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    stdout = models.TextField(blank=True)
    stderr = models.TextField(blank=True)
    return_code = models.IntegerField(blank=True, null=True)
    rendered_code = models.TextField()
    status = models.CharField(max_length=20, db_index=True, default='PENDING')

    desk = models.ForeignKey(Desk)
    contestant = models.ForeignKey(Contestant)
    node = models.ForeignKey(Node)

    def get_execution_dict(self):
        """
        :return: all parameters needed for execute_task function
        """
        return {
            'is_local': self.is_local,
            'ip': self.node.ip,
            'username': self.node.username,
            'rendered_code': self.rendered_code,
            'task_run_id': self.id,
        }

    def duration_milliseconds(self):
        if self.finished_at and self.started_at:
            return (self.finished_at - self.started_at).total_seconds() * 1000
        return 0

    def stop(self):
        self.get_celery_result().revoke()
        if self.status == 'PENDING':
            self.status = 'REVOKED'
            self.save()

    def get_celery_result(self):
        return AsyncResult(self.celery_task)