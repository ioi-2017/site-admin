from django.conf.urls import url

from task_admin.views import RenderPreviewView, CodeRenderView, TaskRunSetsView

urlpatterns = [
    url(r'^render$', RenderPreviewView.as_view(), name='render_preview'),
    url(r'^code_render$', CodeRenderView.as_view(), name='code_render'),
    url(r'^taskrunsets$', TaskRunSetsView.as_view(), name='taskrunsets')
]
