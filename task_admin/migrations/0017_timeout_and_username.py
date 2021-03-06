# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-05 12:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_admin', '0016_auto_20170530_1839'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='timeout',
            field=models.FloatField(default=10.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='username',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='taskrun',
            name='timeout',
            field=models.FloatField(default=10.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taskrun',
            name='username',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='taskrunset',
            name='timeout',
            field=models.FloatField(default=10.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taskrunset',
            name='username',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
