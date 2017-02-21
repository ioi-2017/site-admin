from django.db import models
from django.contrib.auth.models import User
from django_celery_results.models import TaskResult


# Create your models here.
class Task(models.Model):
    is_local = models.BooleanField()
    name = models.CharField(max_length=100)
    code = models.TextField()
    author = models.ForeignKey(User)
    created_at = models.DateTimeField()
    deleted = models.BooleanField()


class TaskRun(models.Model):
    celery_task = models.ForeignKey(TaskResult)

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


