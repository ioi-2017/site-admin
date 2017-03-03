from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic import TemplateView, View
from rest_framework import generics

from task_admin.models import TaskRunSet
from task_admin.serializers import TaskRunSetSerializer
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


class TaskRunSetsAPI(generics.ListCreateAPIView):
    serializer_class = TaskRunSetSerializer

    def get_queryset(self):
        return TaskRunSet.objects.all()


class TaskRunSetsView(ListView):
    template_name = "task_admin/taskrunsets.html"
    queryset = TaskRunSet.objects.all()
