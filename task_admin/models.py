from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Task(models.Model):
    is_local = models.BooleanField()
    name = models.CharField(max_length=100)
    code = models.TextField()
    author = models.ForeignKey(User)
    created_at = models.DateTimeField()
    deleted = models.BooleanField()


class TaskRun(models.Model):
    celery_task = models.CharField(max_length=255, unique=True)
    run_set = models.ForeignKey(TaskRunSet)
    created_at = models.DateTimeField(auto_created=True)

    @property
    def is_done(self):
        raise NotImplemented()

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
