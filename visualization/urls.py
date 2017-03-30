from django.conf.urls import url, include

from visualization.views import RoomView, NodesAPI, DesksAPI, RoomsAPI, ContestantsAPI
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'nodes', NodesAPI)
router.register(r'desks', DesksAPI)
router.register(r'rooms', RoomsAPI)
router.register(r'contestants', ContestantsAPI)

urlpatterns = [
    url(r'^', include(router.urls, namespace='api')),
]
