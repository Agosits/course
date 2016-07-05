# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('selection', '0002_auto_20160705_0255'),
    ]

    operations = [
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='majors',
            field=models.ManyToManyField(to='selection.Major'),
        ),
        migrations.AddField(
            model_name='student',
            name='major',
            field=models.ForeignKey(to='selection.Major', null=True, blank=True),
        ),
    ]
