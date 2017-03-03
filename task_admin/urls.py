from django.conf.urls import url, include

from task_admin.views import RenderPreviewView, CodeRenderView, TaskRunSetsAPI, TaskRunSetsView

api_urlpatterns = [
    url(r'^taskrunsets$', TaskRunSetsAPI.as_view(), name='taskrunsets')
]

urlpatterns = [
    url(r'^render$', RenderPreviewView.as_view(), name='render_preview'),
    url(r'^code_render$', CodeRenderView.as_view(), name='code_render'),
    url(r'^taskrunsets$', TaskRunSetsView.as_view(), name='taskrunsets'),
    url(r'^api/', include(api_urlpatterns, namespace='api')),
]
