# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-09 08:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visualization', '0009_auto_20170308_1908'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalnode',
            name='history_user',
        ),
        migrations.DeleteModel(
            name='HistoricalNode',
        ),
    ]