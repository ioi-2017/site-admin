from django.conf.urls import url, include

from task_admin.views import TaskRunSetsAPI, TasksAPI, TaskRunsAPI, RenderPreviewView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tasks', TasksAPI)
router.register(r'taskruns', TaskRunsAPI)
router.register(r'taskrunsets', TaskRunSetsAPI)

urlpatterns = [
    url(r'^task_create/$', RenderPreviewView.as_view(), name='task_create'),
    url(r'^', include(router.urls, namespace='api')),
]
