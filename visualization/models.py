from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_countries.fields import CountryField
from django.utils.translation import ugettext_lazy as _


class Zone(models.Model):
    name = models.CharField(max_length=40, unique=True)
    width = models.FloatField(default=640)
    height = models.FloatField(default=480)
    desk_width = models.FloatField(default=40)
    desk_height = models.FloatField(default=20)

    def __str__(self):
        return self.name


def xy_range_validator(value):
    if value <= 0 or value >= 1:
        raise ValidationError(
            _('%(value)s must be bigger than 0 and less than 1'),
            params={'value': value},
        )


class Desk(models.Model):
    contestant = models.OneToOneField('Contestant', related_name='desk', blank=True, null=True)
    active_node = models.OneToOneField('Node', related_name='desk', blank=True, null=True)
    zone = models.ForeignKey('Zone', on_delete=models.CASCADE)
    number = models.IntegerField(null=True)
    x = models.FloatField(default=0.5, validators=[xy_range_validator])
    y = models.FloatField(default=0.5, validators=[xy_range_validator])
    angle = models.IntegerField(default=0, validators=[
        MaxValueValidator(359), MinValueValidator(0)
    ])

    class Meta:
        unique_together = ('zone', 'number')

    @property
    def identifier(self):
        return "%s%s" % (self.zone.name, self.number)

    def position_data(self):
        return {
            'x': self.x,
            'y': self.y,
            'angle': self.angle,
            'node': self.active_node.ip,
        }

    def __str__(self):
        return "%s - %s" % (self.contestant.identifier if self.contestant else 'No contestant', self.active_node)


class Team(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    country = CountryField(null=True)
    country_code = models.CharField(max_length=3, null=True, blank=True)

    def __str__(self):
        return self.country_code


class Contestant(models.Model):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=1, choices={'F': 'Female', 'M': 'Male'}.items(), blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    country = CountryField(null=True)
    team = models.ForeignKey('Team', null=True, on_delete=models.CASCADE)
    number = models.IntegerField(default=1)

    class Meta:
        unique_together = ('team', 'number')

    @property
    def team_code(self):
        return self.team.country_code

    @property
    def identifier(self):
        return self.team_code + str(self.number)

    @property
    def name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def __str__(self):
        return "%s - %s" % (self.identifier, self.name)


class Node(models.Model):
    mac_address = models.CharField(max_length=20, unique=True)
    ip = models.GenericIPAddressField(null=True)
    username = models.CharField(max_length=20)
    property_id = models.CharField(max_length=20, unique=True, blank=True)
    connected = models.BooleanField(default=False)
    last_task = models.ForeignKey('task_admin.TaskRun', related_name='node+', blank=True, null=True)

    @property
    def status(self):
        if self.connected is not True:
            return 'DISCONNECTED'
        elif self.last_task is not None:
            return self.last_task.status
        return 'CONNECTED'

    def update_last_task(self):
        self.last_task = self.taskrun_set.filter(task__deleted=False).order_by('-created_at').first()
        self.save()

    @property
    def mac_dash_separated(self):
        return self.mac_address.lower().replace(':', '-')

    def __str__(self):
        return self.ip


class NodeGroup(models.Model):
    name = models.CharField(max_length=40, unique=True)
    expression = models.TextField()

    def nodes(self):
        result = []
        for node in Node.objects.all():
            try:
                if eval(self.expression):
                    result.append(node)
            except:
                continue
        return result

    def __str__(self):
        return self.name
