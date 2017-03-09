from django.conf.urls import url, include

from visualization.views import RoomView, NodesAPI

api_urlpatterns = [
    url(r'^nodes/', NodesAPI.as_view(), name='nodes')
]

urlpatterns = [
    url(r'^$', RoomView.as_view(), name='room'),
    url(r'^api/', include(api_urlpatterns, namespace='api')),
]
