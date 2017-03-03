from celery.result import AsyncResult
from django.contrib.auth.models import User
from django.db import models

from visualization.models import Desk, Node, Contestant


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
    owner = models.ForeignKey(User, related_name='taskrunset', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

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
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField()
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
    def duration(self):
        raise NotImplemented()

    @property
    def started_at(self):
        raise NotImplemented()

    @property
    def finished_at(self):
        raise NotImplemented()
