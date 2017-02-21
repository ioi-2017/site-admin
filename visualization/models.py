from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=40)


class Desk(models.Model):
    contestant = models.OneToOneField('Contestant', related_name='desk')
    active_node = models.OneToOneField('Node', related_name='desk')
    room = models.ForeignKey('Room', on_delete=models.CASCADE)


class Contestant(models.Model):
    name = models.CharField(max_length=100)


class Node(models.Model):
    mac_address = models.CharField(max_length=20)
    ip = models.GenericIPAddressField()
    property_id = models.CharField(max_length=20)
