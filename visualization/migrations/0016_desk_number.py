# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-18 18:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visualization', '0015_auto_20170518_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='desk',
            name='number',
            field=models.IntegerField(null=True),
        ),
    ]
