from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Task, TaskRunSet, TaskRun
from .task_render import render_task
from .tasks import execute_task
from visualization.models import Node


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', 'author', 'code', 'is_local')


class TaskRunSetSerializer(serializers.ModelSerializer):
    owner_data = serializers.StringRelatedField(source='owner')
    task_data = TaskSerializer(source='task', read_only=True)
    taskruns = serializers.StringRelatedField(many=True, read_only=True)
    ips = serializers.ListField(child=serializers.IPAddressField(), write_only=True)

    def create(self, validated_data):
        task = validated_data['task']
        taskrunset = TaskRunSet(
            task=task,
            owner=validated_data['owner']
        )
        taskrunset.save()
        for ip in validated_data['ips']:
            node = get_object_or_404(Node, ip=ip)
            rendered_code = render_task(task.code, {
                'node': node,
                'desk': node.desk,
                'contestant': node.desk.contestant,
            })
            taskrun = TaskRun(
                run_set=taskrunset,
                node=node,
                desk=node.desk,
                contestant=node.desk.contestant,
                rendered_code=rendered_code,
                is_local=task.is_local,
            )
            taskrun.celery_task = execute_task.delay(**taskrun.get_execution_dict()).id
            taskrun.save()
        return taskrunset

    class Meta:
        model = TaskRunSet
        fields = ('task', 'task_data', 'owner', 'owner_data', 'created_at', 'taskruns', 'ips')


class TaskRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskRun
        fields = ()
