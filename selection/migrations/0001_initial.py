# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('compulsory', models.BooleanField(default='False')),
                ('name', models.CharField(max_length=100)),
                ('sid', models.CharField(max_length=20)),
                ('grades', models.CharField(max_length=100)),
                ('power', models.IntegerField(null=True)),
                ('time', models.IntegerField(default=0)),
                ('classroom', models.CharField(default='0-000', max_length=10)),
                ('content', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'ordering': ('sid',),
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=10)),
                ('courses', models.ManyToManyField(to='selection.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('sid', models.CharField(max_length=12)),
                ('cla', models.CharField(max_length=10)),
                ('timetable', models.IntegerField(default=0)),
                ('courses', models.ManyToManyField(blank=True, to='selection.Course')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('sid',),
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('sid', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='teachers',
            field=models.ForeignKey(to='selection.Teacher'),
        ),
    ]
