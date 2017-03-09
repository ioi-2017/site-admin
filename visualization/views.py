from django.shortcuts import render
from django.views import View
from rest_framework import generics

from visualization.models import Room, Node
from visualization.serializers import NodeSerializer


class RoomView(View):
    def get(self, request):
        desks = list(Room.objects.get(id=1).desk_set.all())
        return render(request, 'visualization/basic_room.html', {
            'desks': [desk.position_data() for desk in desks]
        })


class NodesAPI(generics.ListCreateAPIView):
    serializer_class = NodeSerializer

    def get_queryset(self):
        return Node.objects.all()