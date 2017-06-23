import logging

from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.generic import View
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.decorators import detail_route
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet

from task_admin.models import Task, TaskTemplate, TaskRun
from task_admin.serializers import TaskSerializer, TaskTemplateSerializer, TaskRunSerializer
from task_admin.task_render import get_all_possible_vars_sample

logger = logging.getLogger(__name__)


class RenderPreviewView(View):
    def get(self, request):
        response = []
        for template, rendered in get_all_possible_vars_sample().items():
            response.append({'template': template, 'rendered': rendered})
        return JsonResponse(response, safe=False)


class TaskTemplatesAPI(ModelViewSet):
    serializer_class = TaskTemplateSerializer
    filter_fields = ('id', 'name', 'author', 'is_local')
    queryset = TaskTemplate.objects.order_by('-created_at')


class Pagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'


class TaskRunsAPI(ReadOnlyModelViewSet, mixins.ListModelMixin):
    serializer_class = TaskRunSerializer
    filter_fields = ('desk', 'contestant', 'node', 'task', 'status')
    queryset = TaskRun.objects.select_related('task', 'contestant', 'node', 'desk').filter(
        task__deleted=False).order_by(
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


class TaskFilterBackend(DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filter_queryset = super().filter_queryset(request, queryset, view)
        task_state = request.query_params.get('state', None)
        if task_state == 'SUCCESS':
            return filter_queryset.filter(summary__PENDING=0, summary__RUNNING=0, summary__FAILED=0)
        if task_state == 'FINISHED':
            return filter_queryset.filter(summary__PENDING=0, summary__RUNNING=0)
        if task_state == 'RUNNING':
            return filter_queryset.filter(summary__RUNNING__gt=0)
        if task_state == 'PENDING':
            return filter_queryset.filter(summary__RUNNING=0, summary__PENDING__gt=0)
        if task_state == 'ABORTED':
            return filter_queryset.filter(summary__ABORTED__gt=0)
        if task_state == 'FAILED':
            return filter_queryset.filter(summary__FAILED__gt=0)
        return filter_queryset


class TasksAPI(mixins.CreateModelMixin,
               mixins.RetrieveModelMixin,
               mixins.ListModelMixin,
               mixins.DestroyModelMixin,
               GenericViewSet):
    filter_backends = (TaskFilterBackend,)
    pagination_class = Pagination
    serializer_class = TaskSerializer
    filter_fields = ('is_local',)
    queryset = Task.objects.prefetch_related('taskruns', 'taskruns__desk', 'taskruns__node',
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
        logger.info('Task #%d (%s) is deleted' % (instance.id, instance.name))
        for task_run in instance.taskruns.all():
            task_run.stop()
            task_run.node.update_last_task()
        logger.info('Remaining taskruns of Task #%d (%s) has stopped' % (instance.id, instance.name))
        instance.save()

    @detail_route(methods=['post'])
    def stop(self, request, pk):
        task = self.get_object()
        logger.info('Task #%d (%s) is going to stop' % (task.id, task.name))
        for taskrun in task.taskruns.all():
            taskrun.stop()
        logger.info('Task #%d (%s) has stopped' % (task.id, task.name))
        return HttpResponse('', status=204)
