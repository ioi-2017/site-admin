from django.contrib import admin
from . import models

admin.site.register(models.Contestant)
admin.site.register(models.Zone)
admin.site.register(models.Node)
admin.site.register(models.Desk)
admin.site.register(models.NodeGroup)
