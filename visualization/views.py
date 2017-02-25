from django.shortcuts import render
from django.views import View

from visualization.models import Room


class RoomView(View):
    def get(self, request):
        desks = list(Room.objects.get(id=1).desk_set.all())
        return render(request, 'visualization/basic_room.html', {
            'desks': [desk.position_data() for desk in desks]
        })
