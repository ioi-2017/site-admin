from django.conf.urls import url, include

from ping.views import PingLogsAPI
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'pinglogs', PingLogsAPI)

urlpatterns = [
    url(r'^', include(router.urls, namespace='api')),
]
