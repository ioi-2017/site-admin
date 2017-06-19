import logging

from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.generic import View
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.decorators import detail_route
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet

from task_admin.models import TaskRunSet, Task, TaskRun
from task_admin.serializers import TaskRunSetSerializer, TaskSerializer, TaskRunSerializer
from task_admin.task_render import get_all_possible_vars_sample

logger = logging.getLogger(__name__)


class RenderPreviewView(View):
    def get(self, request):
        response = []
        for template, rendered in get_all_possible_vars_sample().items():
            response.append({'template': template, 'rendered': rendered})
        return JsonResponse(response, safe=False)


class TasksAPI(ModelViewSet):
    serializer_class = TaskSerializer
    filter_fields = ('id', 'name', 'author', 'is_local')
    queryset = Task.objects.order_by('-created_at')


class Pagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'


class TaskRunsAPI(ReadOnlyModelViewSet, mixins.ListModelMixin):
    serializer_class = TaskRunSerializer
    filter_fields = ('desk', 'contestant', 'node', 'run_set', 'status')
    queryset = TaskRun.objects.select_related('run_set', 'contestant', 'node', 'desk').filter(
        run_set__deleted=False).order_by(
        '-created_at')
    pagination_class = Pagination

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['pagination'] = self.paginator.get_html_context()
        return response

    @detail_route(methods=['post'])
    def stop(self, request, pk):
        task_run = self.get_object()
        task_run.stop()
        logger.info('Taskrun #%d has stopped' % task_run.id)
        return HttpResponse('', status=204)


class TaskRunSetFilterBackend(DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filter_queryset = super().filter_queryset(request, queryset, view)
        runset_state = request.query_params.get('state', None)
        if runset_state == 'SUCCESS':
            return filter_queryset.filter(summary__PENDING=0, summary__RUNNING=0, summary__FAILED=0)
        if runset_state == 'FINISHED':
            return filter_queryset.filter(summary__PENDING=0, summary__RUNNING=0)
        if runset_state == 'RUNNING':
            return filter_queryset.filter(summary__RUNNING__gt=0)
        if runset_state == 'PENDING':
            return filter_queryset.filter(summary__RUNNING=0, summary__PENDING__gt=0)
        if runset_state == 'ABORTED':
            return filter_queryset.filter(summary__ABORTED__gt=0)
        if runset_state == 'FAILED':
            return filter_queryset.filter(summary__FAILED__gt=0)
        return filter_queryset


class TaskRunSetsAPI(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    filter_backends = (TaskRunSetFilterBackend,)
    pagination_class = Pagination
    serializer_class = TaskRunSetSerializer
    filter_fields = ('is_local',)
    queryset = TaskRunSet.objects.prefetch_related('taskruns', 'taskruns__desk', 'taskruns__node',
                                                   'taskruns__contestant').select_related('owner').filter(
        deleted=False).order_by('-created_at')
    max_page_size = 10000

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['pagination'] = self.paginator.get_html_context()
        return response

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
        logger.info('Taskrunset #%d (%s) is deleted' % (instance.id, instance.name))
        for task_run in instance.taskruns.all():
            task_run.stop()
            task_run.node.update_last_task()
        logger.info('Remaining taskruns of Taskrunset #%d (%s) has stopped' % (instance.id, instance.name))
        instance.save()

    @detail_route(methods=['post'])
    def stop(self, request, pk):
        task_runset = self.get_object()
        logger.info('Taskrunset #%d (%s) is going to stop' % (task_runset.id, task_runset.name))
        for task_run in task_runset.taskruns.all():
            task_run.stop()
        logger.info('Taskrunset #%d (%s) has stopped' % (task_runset.id, task_runset.name))
        return HttpResponse('', status=204)
