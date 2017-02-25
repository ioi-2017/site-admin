from django.contrib import admin
from . import models

admin.site.register(models.Contestant)
admin.site.register(models.Room)
admin.site.register(models.Node)
admin.site.register(models.Desk)
