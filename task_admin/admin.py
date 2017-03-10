from django.contrib import admin
from . import models


class TaskRunAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'created_at', 'is_local', 'node', 'desk', 'contestant', 'is_successful')


class TaskRunSetAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'created_at', 'task', 'number_of_nodes', 'owner')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'created_at', 'name', 'is_local', 'author', 'deleted')


admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.TaskRun, TaskRunAdmin)
admin.site.register(models.TaskRunSet, TaskRunSetAdmin)
