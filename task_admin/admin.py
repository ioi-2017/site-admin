from django.contrib import admin
from . import models


class TaskRunAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'is_local', 'node', 'desk', 'contestant', 'is_successful')


admin.site.register(models.Task)
admin.site.register(models.TaskRun, TaskRunAdmin)
admin.site.register(models.TaskRunSet)
