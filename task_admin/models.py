from django.db import models
from django.contrib.auth.models import User
from visualization.models import Desk, Node, Contestant
from celery.result import AsyncResult


class Task(models.Model):
    is_local = models.BooleanField()
    name = models.CharField(max_length=100)
    code = models.TextField()
    author = models.ForeignKey(User)
    created_at = models.DateTimeField()
    deleted = models.BooleanField()


def render_task(task, context):
    """

    :param task: single instance of Task model
    :param context: context to format code, usually with node, desk and contestant
    :return: rendered code of task
    """
    code = task.code
    return code.format(**context)


class TaskRunSet(models.Model):
    task = models.ForeignKey(Task)
    created_at = models.DateTimeField()

    @property
    def finished_at(self):
        # finished_at = 0
        # for task_run in self.taskrun_set.all():
        #     finished_at = max(finished_at, task_run.finished_at)
        # return finished_at
        raise NotImplemented()


class TaskRun(models.Model):
    celery_task = models.CharField(max_length=255, unique=True)
    run_set = models.ForeignKey(TaskRunSet)
    created_at = models.DateTimeField(auto_created=True)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField()
    rendered_code = models.TextField()

    desk = models.ForeignKey(Desk)
    contestant = models.ForeignKey(Contestant)
    node = models.ForeignKey(Node)

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
