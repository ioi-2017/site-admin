# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-30 18:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task_admin', '0015_taskrunset_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskrun',
            name='contestant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='visualization.Contestant'),
        ),
        migrations.AlterField(
            model_name='taskrun',
            name='desk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='visualization.Desk'),
        ),
    ]