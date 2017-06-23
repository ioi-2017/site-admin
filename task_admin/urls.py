from django.conf.urls import url, include

from task_admin.views import TasksAPI, TaskTemplatesAPI, TaskRunsAPI, RenderPreviewView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'templates', TaskTemplatesAPI)
router.register(r'taskruns', TaskRunsAPI)
router.register(r'tasks', TasksAPI)

urlpatterns = [
    url(r'^task_create/$', RenderPreviewView.as_view(), name='task_create'),
    url(r'^', include(router.urls, namespace='api')),
]
