from django.conf.urls import url

from task_admin.views import RenderPreviewView, CodeRenderView, TaskRunSetsView, TaskView

urlpatterns = [
    url(r'^task_create$', RenderPreviewView.as_view(), name='task_create'),
    url(r'^code_render$', CodeRenderView.as_view(), name='code_render'),
    url(r'^taskrunsets$', TaskRunSetsView.as_view(), name='taskrunsets'),
    url(r'^tasks$', TaskView.as_view(), name='tasks'),
]
