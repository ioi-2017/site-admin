from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_countries.fields import CountryField


class Room(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name


class Desk(models.Model):
    contestant = models.OneToOneField('Contestant', related_name='desk')
    active_node = models.OneToOneField('Node', related_name='desk')
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    x = models.DecimalField(max_digits=5, decimal_places=5, default=0)
    y = models.DecimalField(max_digits=5, decimal_places=5, default=0)
    angle = models.IntegerField(default=0, validators=[
        MaxValueValidator(359), MinValueValidator(0)
    ])

    def __str__(self):
        return "%s - %s" % (self.contestant.identifier, self.active_node)


class Contestant(models.Model):
    name = models.CharField(max_length=100)
    country = CountryField(null=True)
    number = models.IntegerField(default=1, unique=True)

    @property
    def identifier(self):
        return self.country.alpha3 + str(self.number)

    def __str__(self):
        return "%s - %s" % (self.identifier, self.name)


class Node(models.Model):
    mac_address = models.CharField(max_length=20, unique=True)
    ip = models.GenericIPAddressField()
    username = models.CharField(max_length=20)
    property_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.ip