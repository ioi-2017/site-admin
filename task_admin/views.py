import django_filters
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView, View
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet

from task_admin.models import TaskRunSet, Task, TaskRun
from task_admin.serializers import TaskRunSetSerializer, TaskSerializer, TaskRunSerializer
from task_admin.task_render import get_all_possible_vars, render_preview


class RenderPreviewView(TemplateView):
    template_name = "task_admin/render_preview.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(help_table=sorted(get_all_possible_vars().items()), **kwargs)


class CodeRenderView(View):
    def get(self, request):
        try:
            result = render_preview(request.GET['code'])
        except:
            result = 'Invalid code'
        return HttpResponse(result)


class TaskRunSetsView(ListView):
    template_name = "task_admin/taskrunsets.html"
    queryset = TaskRunSet.objects.all()


class TasksAPI(ModelViewSet):
    serializer_class = TaskSerializer
    filter_fields = ('id', 'name', 'author', 'is_local')
    queryset = Task.objects.all()


class TaskRunsAPI(ReadOnlyModelViewSet):
    serializer_class = TaskRunSerializer
    filter_fields = ('desk', 'contestant', 'node')
    queryset = TaskRun.objects.all()


class TaskRunSetPagination(PageNumberPagination):
    page_size = 5


class TaskRunSetFilterBackend(DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filter_queryset = super().filter_queryset(request, queryset, view)
        runset_state = request.query_params.get('state', None)
        if runset_state == 'finished':
            return [runset for runset in filter_queryset if runset.is_finished]
        return filter_queryset

class TaskRunSetsAPI(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    filter_backends = (TaskRunSetFilterBackend,)
    pagination_class = TaskRunSetPagination
    serializer_class = TaskRunSetSerializer
    filter_fields = ('is_local',)
    queryset = TaskRunSet.objects.all()
    max_page_size = 10000

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['pagination'] = self.paginator.get_html_context()
        return response
