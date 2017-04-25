from django.contrib.auth.models import User
from django.db import models

from visualization.models import Desk, Node, Contestant


class PingLog(models.Model):
    node = models.ForeignKey(Node)
    event_time = models.DateTimeField(auto_now_add=True)
    connected = models.BooleanField()

    def __str__(self):
        return "Node %s %s at %s" % (self.node, ('connected' if self.connected else 'disconnected'), self.event_time)
