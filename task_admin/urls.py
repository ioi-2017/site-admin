from django.conf.urls import url, include

from task_admin.views import RenderPreviewView, CodeRenderView, TaskRunSetsAPI, TaskRunSetsView, TasksAPI, TaskRunsAPI, \
    TaskRunsView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tasks', TasksAPI)
router.register(r'taskruns', TaskRunsAPI)
router.register(r'taskrunsets', TaskRunSetsAPI)

urlpatterns = [
    url(r'^task_create$', RenderPreviewView.as_view(), name='task_create'),
    url(r'^code_render$', CodeRenderView.as_view(), name='code_render'),
    url(r'^taskrunsets$', TaskRunSetsView.as_view(), name='taskrunsets'),
    url(r'^taskruns$', TaskRunsView.as_view(), name='taskruns'),
    url(r'^api/', include(router.urls, namespace='api')),
]
