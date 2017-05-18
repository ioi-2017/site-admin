import svgwrite
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from django.views import View
from rest_framework.viewsets import ModelViewSet

from visualization.models import Room, Node, Desk, Contestant
from visualization.serializers import NodeSerializer, DeskSerializer, ContestantSerializer, RoomSerializer


class RetrieveIPView(View):
    def get(self, request, ip):
        node = Node.objects.get(ip=ip)
        desk = node.desk
        contestant = desk.contestant
        return JsonResponse({
            'node': {
                'ip': node.ip,
                'mac': node.mac_address,
            },
            'contestant': {
                'name': contestant.name,
                'country': contestant.country.name,
                'number': contestant.number,
                'id': contestant.identifier,
            },
            'desk': {
                'room': desk.room.name,
                'map': reverse('visualization:node-map', kwargs={'ip': ip}),
            },
        }, safe=False)


class RetrieveDeskMap(View):
    def get(self, request, ip):
        image = svgwrite.Drawing(size=("300px", "240px"))
        return HttpResponse(image.tostring(), content_type="image/svg+xml")


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
