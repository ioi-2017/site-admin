from django.contrib import admin
from . import models


class TaskRunAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'created_at', 'is_local', 'node', 'desk', 'contestant', 'status')


class TaskRunSetAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'created_at', 'number_of_nodes', 'owner')


class TaskTemplateAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'created_at', 'name', 'is_local', 'author', 'deleted')


admin.site.register(models.TaskTemplate, TaskTemplateAdmin)
admin.site.register(models.TaskRun, TaskRunAdmin)
admin.site.register(models.TaskRunSet, TaskRunSetAdmin)
