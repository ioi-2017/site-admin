from rest_framework import serializers

from task_admin.models import Task, TaskRunSet, TaskRun
from task_admin.task_render import render_task
from task_admin.tasks import execute_task, add_time
from visualization.models import Node


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', 'author', 'code', 'is_local')


class TaskRunSetSerializer(serializers.ModelSerializer):
    owner_data = serializers.StringRelatedField(source='owner')
    task_data = TaskSerializer(source='task', read_only=True)
    taskruns = serializers.StringRelatedField(many=True, read_only=True)
    ips = serializers.JSONField(write_only=True)

    def create(self, validated_data):
        task = validated_data['task']
        taskrunset = TaskRunSet(
            task=task,
            owner=validated_data['owner']
        )
        taskrunset.save()
        for ip in validated_data['ips']:
            node = Node.objects.get(ip=ip)
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
            taskrun.celery_task = add_time(execute_task.s(**taskrun.get_execution_dict())).delay().id
            taskrun.save()
        return taskrunset

    class Meta:
        model = TaskRunSet
        fields = ('id', 'task', 'task_data', 'owner', 'owner_data', 'created_at', 'taskruns', 'ips')


class TaskRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskRun
        fields = (
            'id', 'celery_task', 'is_local', 'run_set', 'created_at', 'started_at', 'finished_at', 'rendered_code',
            'desk', 'contestant', 'node')
