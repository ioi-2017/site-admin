# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-18 18:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualization', '0016_desk_number'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='desk',
            unique_together=set([('room', 'number')]),
        ),
    ]
