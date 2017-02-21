from django.conf.urls import url

from visualization.views import RoomView

urlpatterns = [
    url(r'^$', RoomView.as_view(), name='room'),
]
