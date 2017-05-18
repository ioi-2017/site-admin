from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_countries.fields import CountryField
from simple_history.models import HistoricalRecords
from django.utils.translation import ugettext_lazy as _


class Room(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name


def xy_range_validator(value):
    if value <= 0 or value >= 1:
        raise ValidationError(
            _('%(value)s must be bigger than 0 and less than 1'),
            params={'value': value},
        )


class Desk(models.Model):
    contestant = models.OneToOneField('Contestant', related_name='desk', null=True)
    active_node = models.OneToOneField('Node', related_name='desk', null=True)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    x = models.FloatField(default=0.5, validators=[xy_range_validator])
    y = models.FloatField(default=0.5, validators=[xy_range_validator])
    angle = models.IntegerField(default=0, validators=[
        MaxValueValidator(359), MinValueValidator(0)
    ])

    def position_data(self):
        return {
            'x': self.x,
            'y': self.y,
            'angle': self.angle,
            'node': self.active_node.ip,
        }

    def __str__(self):
        return "%s - %s" % (self.contestant.identifier, self.active_node)


class Contestant(models.Model):
    name = models.CharField(max_length=100)
    country = CountryField(null=True)
    number = models.IntegerField(default=1)

    class Meta:
        unique_together = ('country', 'number')

    @property
    def identifier(self):
        return self.country.alpha3 + str(self.number)

    def __str__(self):
        return "%s - %s" % (self.identifier, self.name)


class Node(models.Model):
    mac_address = models.CharField(max_length=20, unique=True)
    ip = models.GenericIPAddressField()
    username = models.CharField(max_length=20)
    property_id = models.CharField(max_length=20, unique=True, null=True)
    connected = models.BooleanField(default=False)

    # history = HistoricalRecords()

    def __str__(self):
        return self.ip
