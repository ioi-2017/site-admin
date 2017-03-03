from rest_framework import serializers

from task_admin.models import Task, TaskRunSet


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('name', 'author', 'code', 'is_local')


class TaskRunSetSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    task = serializers.StringRelatedField()

    class Meta:
        model = TaskRunSet
        fields = ('task', 'owner', 'created_at')
