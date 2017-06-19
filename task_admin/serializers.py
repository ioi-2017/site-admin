import logging
from rest_framework import serializers
from rest_framework.exceptions import APIException
from task_admin.models import Task, TaskRunSet, TaskRun
from task_admin.task_render import render_task
from task_admin.tasks import execute_task
from visualization.models import Node, Desk, Contestant
from visualization.serializers import NodeSerializer, DeskSerializer, ContestantSerializer

logger = logging.getLogger(__name__)


class BadRequest(APIException):
    status_code = 400


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', 'author', 'code', 'is_local', 'timeout', 'username')


class TaskRunSetSerializer(serializers.ModelSerializer):
    owner_data = serializers.StringRelatedField(source='owner')
    taskruns = serializers.StringRelatedField(many=True, read_only=True)
    ips = serializers.JSONField(write_only=True)
    code = serializers.CharField(required=True)
    is_local = serializers.BooleanField(required=True)
    timeout = serializers.FloatField(required=True)
    username = serializers.CharField(required=True, allow_blank=True)
    name = serializers.CharField(required=True)

    def create(self, data):
        for ip in data['ips']:
            try:
                node = Node.objects.get(ip=ip)
            except Node.DoesNotExist:
                raise BadRequest(detail=(u"Ip {0:s} doesn't exist".format(ip)), code=400)
            render_task(data['code'], node)  # Ensure render doesn't throw exception

        taskrunset = TaskRunSet(
            code=data['code'],
            is_local=data['is_local'],
            timeout=data['timeout'],
            username=data['username'],
            owner=data['owner'],
            name=data['name'],
            summary={'PENDING': len(data['ips']),
                     'SUCCESS': 0,
                     'REVOKED': 0,
                     'FAILURE': 0,
                     'PROGRESS': 0}
        )
        taskrunset.save()  # TODO: Taskrunset should not be created unless all taskruns created successfully
        logger.info('Taskrunset #%d (%s) is going to be created' % (taskrunset.id, taskrunset.name))
        for ip in data['ips']:
            node = Node.objects.get(ip=ip)
            rendered_code = render_task(data['code'], node)
            taskrun = TaskRun(
                run_set=taskrunset,
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
        logger.info('Taskrunset #%d (%s) has created' % (taskrunset.id, taskrunset.name))
        return taskrunset

    class Meta:
        model = TaskRunSet
        fields = (
            'id', 'code', 'is_local', 'timeout', 'username', 'name', 'owner', 'owner_data', 'created_at', 'taskruns',
            'ips', 'results', 'summary', 'is_finished')


class TaskRunSerializer(serializers.ModelSerializer):
    node = NodeSerializer(read_only=True)
    desk = DeskSerializer(read_only=True)
    contestant = ContestantSerializer(read_only=True)

    class Meta:
        model = TaskRun
        fields = (
            'id', 'celery_task', 'is_local', 'timeout', 'username', 'run_set', 'created_at', 'started_at',
            'finished_at', 'rendered_code', 'duration_milliseconds', 'stdout', 'stderr', 'return_code', 'status',
            'desk', 'contestant', 'node')
