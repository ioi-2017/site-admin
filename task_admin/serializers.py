import logging

from rest_framework import serializers
from rest_framework.exceptions import APIException

from task_admin.models import TaskTemplate, Task, TaskRun
from task_admin.task_render import render_task
from task_admin.tasks import execute_task
from visualization.models import Node
from visualization.serializers import NodeSerializer, DeskSerializer, ContestantSerializer

logger = logging.getLogger(__name__)


class BadRequest(APIException):
    status_code = 400


def create_task(data):
    for ip in data['ips']:
        try:
            node = Node.objects.get(ip=ip)
        except Node.DoesNotExist:
            raise Exception(detail=(u"Ip {0:s} doesn't exist".format(ip)), code=400)
        render_task(data['code'], node)

    task = Task(
        code=data['code'],
        is_local=data['is_local'],
        timeout=data['timeout'],
        username=data['username'],
        owner=data['owner'],
        name=data['name'],
        summary={'PENDING': len(data['ips']),
                 'SUCCESS': 0,
                 'ABORTED': 0,
                 'FAILED': 0,
                 'RUNNING': 0}
    )
    task.save()  # TODO: Task should not be created unless all taskruns created successfully
    logger.info('Task #%d (%s) is going to be created' % (task.id, task.name))
    for ip in data['ips']:
        node = Node.objects.get(ip=ip)
        rendered_code = render_task(data['code'], node)
        taskrun = TaskRun(
            task=task,
            node=node,
            desk=node.desk if hasattr(node, 'desk') else None,
            contestant=node.desk.contestant if hasattr(node, 'desk') and hasattr(node.desk, 'contestant') else None,
            rendered_code=rendered_code,
            is_local=data['is_local'],
            timeout=data['timeout'],
            username=data['username']
        )
        taskrun.save()

        node.last_task = taskrun
        node.save()

        taskrun.celery_task = execute_task.apply_async(
            queue='local_queue' if data['is_local'] else 'remote_queue'
            , kwargs=taskrun.get_execution_dict()).id
        taskrun.save(update_fields=['celery_task'])
    logger.info('Task #%d (%s) has created' % (task.id, task.name))
    return task


class TaskTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTemplate
        fields = ('id', 'name', 'author', 'code', 'is_local', 'timeout', 'username')


class TaskSerializer(serializers.ModelSerializer):
    owner_data = serializers.StringRelatedField(source='owner')
    ips = serializers.JSONField(write_only=True)
    summary = serializers.JSONField(read_only=True)
    code = serializers.CharField(required=True)
    is_local = serializers.BooleanField(required=True)
    timeout = serializers.FloatField(required=True)
    username = serializers.CharField(required=True, allow_blank=True)
    name = serializers.CharField(required=True)

    def create(self, data):
        try:
            task = create_task(data)
        except Exception as e:
            raise BadRequest(detail=str(e))
        return task

    class Meta:
        model = Task
        fields = (
            'id', 'code', 'is_local', 'timeout', 'username', 'name', 'owner', 'owner_data', 'created_at',
            'ips', 'summary', 'is_finished')


class TaskRunSerializer(serializers.ModelSerializer):
    node = NodeSerializer(read_only=True)
    desk = DeskSerializer(read_only=True)
    contestant = ContestantSerializer(read_only=True)

    class Meta:
        model = TaskRun
        fields = (
            'id', 'celery_task', 'is_local', 'timeout', 'username', 'task', 'task_name', 'created_at', 'started_at',
            'finished_at', 'rendered_code', 'duration_milliseconds', 'stdout', 'stderr', 'return_code', 'status',
            'desk', 'contestant', 'node')
