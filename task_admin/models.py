import textwrap

from celery.result import AsyncResult
from django.contrib.auth.models import User
from django.db import models

from dateutil.parser import parser

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
    is_local = models.BooleanField()
    code = models.TextField()
    owner = models.ForeignKey(User, related_name='taskrunset', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def last_finished_at(self):
        return max(task_run.finished_at for task_run in self.taskruns.all())

    @property
    def max_duration_milliseconds(self):
        return max(task_run.duration_milliseconds for task_run in self.taskruns.all())

    @property
    def results(self):
        return [task_run.result for task_run in self.taskruns.all()]

    def number_of_nodes(self):
        return self.taskruns.count()

    def __str__(self):
        return '[%s] on %d nodes' % (textwrap.shorten(self.code, 10), self.number_of_nodes())


class TaskRun(models.Model):
    celery_task = models.CharField(max_length=255, unique=True)
    is_local = models.BooleanField()
    run_set = models.ForeignKey(TaskRunSet, related_name='taskruns')
    created_at = models.DateTimeField(auto_now_add=True)
    rendered_code = models.TextField()

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
            'rendered_code': self.rendered_code
        }

    def get_celery_result(self):
        return AsyncResult(self.celery_task)

    def is_successful(self):
        return self.get_celery_result().successful()

    is_successful.boolean = True

    @property
    def duration_milliseconds(self):
        return self.get_celery_result().get()['duration_milliseconds']

    @property
    def started_at(self):
        return parser().parse(self.get_celery_result().get()['started_at'])

    @property
    def finished_at(self):
        return parser().parse(self.get_celery_result().get()['finished_at'])

    @property
    def result(self):
        return self.get_celery_result().get()['result']

    def __str__(self):
        return '[%s] on %s' % (textwrap.shorten(self.run_set.code, 10), self.node.ip)
