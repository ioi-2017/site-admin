from django.db import models


class Room(models.Model):
    pass


class Desk(models.Model):
    contestant = models.OneToOneField('Contestant', related_name='desk')
    node = models.OneToOneField('Node', related_name='desk')


class Contestant(models.Model):
    name = models.CharField()


class Node(models.Model):
    mac_address = models.CharField()
    ip = models.IPAddressField()