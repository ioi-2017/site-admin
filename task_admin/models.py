import textwrap
from collections import Counter

from celery.result import AsyncResult
from django.contrib.auth.models import User
from django.db import models, transaction, connection
from django.contrib.postgres.fields import JSONField

from visualization.models import Desk, Node, Contestant


class TaskTemplate(models.Model):
    is_local = models.BooleanField()
    timeout = models.FloatField()
    username = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100)
    code = models.TextField()
    author = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return '[%s] by %s' % (self.name, self.author)


class Task(models.Model):
    name = models.TextField(blank=True)
    is_local = models.BooleanField()
    timeout = models.FloatField()
    username = models.CharField(max_length=20, blank=True, null=True)
    code = models.TextField()
    owner = models.ForeignKey(User, related_name='task', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    summary = JSONField()

    @property
    def last_finished_at(self):
        return max(task_run.finished_at for task_run in self.taskruns.all())

    @property
    def max_duration_milliseconds(self):
        return max(task_run.duration_milliseconds for task_run in self.taskruns.all())

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
    timeout = models.FloatField()
    username = models.CharField(max_length=20, blank=True, null=True)
    task = models.ForeignKey(Task, related_name='taskruns')
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    stdout = models.TextField(blank=True)
    stderr = models.TextField(blank=True)
    return_code = models.IntegerField(blank=True, null=True)
    rendered_code = models.TextField()
    status = models.CharField(max_length=20, db_index=True, default='PENDING')

    desk = models.ForeignKey(Desk, null=True)
    contestant = models.ForeignKey(Contestant, null=True)
    node = models.ForeignKey(Node)

    def get_execution_dict(self):
        """
        :return: all parameters needed for execute_task function
        """
        return {
            'is_local': self.is_local,
            'timeout': self.timeout,
            'username': self.username or self.node.username,
            'ip': self.node.ip,
            'rendered_code': self.rendered_code,
            'task_run_id': self.id
        }

    def duration_milliseconds(self):
        if self.finished_at and self.started_at:
            return (self.finished_at - self.started_at).total_seconds() * 1000
        return 0

    def stop(self):
        self.get_celery_result().revoke()
        if self.get_celery_result().status == 'PENDING':
            with transaction.atomic():
                self.change_status('ABORTED')
                self.save()

    @transaction.atomic
    def change_status(self, new_status):
        if new_status == self.status:
            return
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE task_admin_task set summary = summary || "
            "jsonb_build_object('{0}',(summary->>'{0}')::int-1) ||"
            "jsonb_build_object('{1}',(summary->>'{1}')::int+1) "
            "where id={2};".format(self.status, new_status, self.task_id))
        self.status = new_status

    def get_celery_result(self):
        return AsyncResult(self.celery_task)
