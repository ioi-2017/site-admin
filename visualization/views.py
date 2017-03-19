from django.shortcuts import render
from django.views import View
from rest_framework.viewsets import ModelViewSet

from visualization.models import Room, Node, Desk, Contestant
from visualization.serializers import NodeSerializer, DeskSerializer, ContestantSerializer, RoomSerializer


class RoomView(View):
    def get(self, request):
        desks = list(Room.objects.get(id=1).desk_set.all())
        return render(request, 'visualization/basic_room.html', {
            'desks': [desk.position_data() for desk in desks]
        })


class NodesAPI(ModelViewSet):
    serializer_class = NodeSerializer
    filter_fields = ('id', 'ip', 'mac_address', 'username', 'property_id', 'connected')
    queryset = Node.objects.all()


class DesksAPI(ModelViewSet):
    serializer_class = DeskSerializer
    filter_fields = ('contestant', 'active_node', 'room',)
    queryset = Desk.objects.all()


class ContestantsAPI(ModelViewSet):
    serializer_class = ContestantSerializer
    filter_fields = ('country', 'number',)
    queryset = Contestant.objects.all()


class RoomsAPI(ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
