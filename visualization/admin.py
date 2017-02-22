from django.contrib import admin

from visualization.models import Desk, Node, Contestant, Room

admin.site.register(Room)
admin.site.register(Desk)
admin.site.register(Node)
admin.site.register(Contestant)
