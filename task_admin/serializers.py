from rest_framework import serializers
from rest_framework.exceptions import APIException

from task_admin.models import Task, TaskRunSet, TaskRun
from task_admin.task_render import render_task
from task_admin.tasks import execute_task
from visualization.models import Node, Desk, Contestant
from visualization.serializers import NodeSerializer, DeskSerializer, ContestantSerializer


class BadRequest(APIException):
    status_code = 400


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', 'author', 'code', 'is_local')


class TaskRunSetSerializer(serializers.ModelSerializer):
    owner_data = serializers.StringRelatedField(source='owner')
    taskruns = serializers.StringRelatedField(many=True, read_only=True)
    ips = serializers.JSONField(write_only=True)
    task = serializers.IntegerField(required=False, write_only=True)
    code = serializers.CharField(required=False)
    is_local = serializers.BooleanField(required=False)

    def create(self, validated_data):
        indirect_code_provided = False
        direct_code_provided = False
        code = validated_data.get('code', None)
        is_local = validated_data.get('is_local', None)
        if code and is_local != None:
            direct_code_provided = True
        elif code or is_local:
            raise BadRequest(detail='Provide both code and is_local or none of them')
        task_id = validated_data.get('task', None)
        if task_id:
            indirect_code_provided = True
            try:
                task = Task.objects.get(pk=task_id)
            except Task.DoesNotExist:
                raise BadRequest(detail="Task id provided doesn't exist", code=400)
            code, is_local = task.code, task.is_local

        if indirect_code_provided and direct_code_provided:
            raise BadRequest(detail="Both task and code are provided, can't decide which to use", code=400)
        elif not (indirect_code_provided or direct_code_provided):
            raise BadRequest(detail="Neither task or code is provided", code=400)

        for ip in validated_data['ips']:
            try:
                Node.objects.get(ip=ip).desk.contestant
            except Node.DoesNotExist:
                raise BadRequest(detail=(u"Ip {0:s} doesn't exist".format(ip)), code=400)
            except Desk.DoesNotExist:
                raise BadRequest(detail=(u"Ip {0:s} provided is attached to no desks".format(ip)), code=400)
            except Contestant.DoesNotExist:
                raise BadRequest(detail=(u"IP {0:s} is not used by anyone".format(ip)), code=400)

        taskrunset = TaskRunSet(
            code=code,
            is_local=is_local,
            owner=validated_data['owner']
        )
        taskrunset.save()
        for ip in validated_data['ips']:
            node = Node.objects.get(ip=ip)
            rendered_code = render_task(code, {
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
                is_local=is_local,
            )

            taskrun.celery_task = execute_task.apply_async(queue='local_queue' if is_local else 'remote_queue'
                                                           , kwargs=taskrun.get_execution_dict()).id
            taskrun.save()
        return taskrunset

    class Meta:
        model = TaskRunSet
        fields = (
            'id', 'code', 'is_local', 'owner', 'owner_data', 'created_at', 'taskruns', 'ips', 'task', 'results',
            'summary', 'is_finished')


class TaskRunSerializer(serializers.ModelSerializer):
    node = NodeSerializer(read_only=True)
    desk = DeskSerializer(read_only=True)
    contestant = ContestantSerializer(read_only=True)

    class Meta:
        model = TaskRun
        fields = (
            'id', 'celery_task', 'is_local', 'run_set', 'created_at', 'started_at', 'finished_at',
            'duration_milliseconds', 'rendered_code', 'result', 'status',
            'desk', 'contestant', 'node')
