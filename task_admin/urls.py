from django.conf.urls import url, include

from task_admin.views import TaskRunSetsAPI, TasksAPI, TaskRunsAPI

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tasks', TasksAPI)
router.register(r'taskruns', TaskRunsAPI)
router.register(r'taskrunsets', TaskRunSetsAPI)

urlpatterns = [
    url(r'^', include(router.urls, namespace='api')),
]
