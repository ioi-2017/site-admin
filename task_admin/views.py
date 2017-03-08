from django.http import HttpResponse
from django.views.generic import ListView, TemplateView, View
from rest_framework import generics

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


class TasksAPI(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.all()


class TaskRunsAPI(generics.ListAPIView):
    serializer_class = TaskRunSerializer

    def get_queryset(self):
        return TaskRun.objects.all()


class TaskRunSetsAPI(generics.ListCreateAPIView):
    serializer_class = TaskRunSetSerializer

    def get_queryset(self):
        return TaskRunSet.objects.all()
