from rest_framework import serializers

from task_admin.models import Task, TaskRunSet


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('name', 'author', 'code', 'is_local')


class TaskRunSetSerializer(serializers.ModelSerializer):
    owner_data = serializers.StringRelatedField(source='owner')
    task_data = serializers.StringRelatedField(source='task')
    taskruns = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = TaskRunSet
        fields = ('task', 'task_data', 'owner', 'owner_data', 'created_at', 'taskruns')
