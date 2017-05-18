from django.conf.urls import url, include

from visualization.views import NodesAPI, DesksAPI, RoomsAPI, ContestantsAPI, RetrieveIPView, RetrieveDeskMap
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'nodes', NodesAPI)
router.register(r'desks', DesksAPI)
router.register(r'rooms', RoomsAPI)
router.register(r'contestants', ContestantsAPI)

urlpatterns = [
    url(r'^nodes/ip/(?P<ip>[0-9.]+)/$', RetrieveIPView.as_view(), name='node-info'),
    url(r'^nodes/ip/(?P<ip>[0-9.]+)/map/$', RetrieveDeskMap.as_view(), name='node-map'),
    url(r'^', include(router.urls, namespace='api')),
]
