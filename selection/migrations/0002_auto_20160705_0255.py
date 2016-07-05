# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('selection', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='teachers',
        ),
        migrations.RemoveField(
            model_name='grade',
            name='courses',
        ),
        migrations.AddField(
            model_name='student',
            name='grade',
            field=models.ForeignKey(null=True, blank=True, to='selection.Grade'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='courses',
            field=models.ManyToManyField(to='selection.Course', blank=True),
        ),
        migrations.RemoveField(
            model_name='course',
            name='grades',
        ),
        migrations.AddField(
            model_name='course',
            name='grades',
            field=models.ManyToManyField(to='selection.Grade'),
        ),
    ]
