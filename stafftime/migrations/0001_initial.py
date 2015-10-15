# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DateSearch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_search', models.DateTimeField(verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb9\xd1\x82\xd0\xb8 \xd0\xbf\xd0\xbe \xd0\xb4\xd0\xb0\xd1\x82\xd0\xb5:')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300, verbose_name=b'\xd0\x9e\xd1\x82\xd0\xb4\xd0\xb5\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=250, verbose_name=b'\xd0\x98\xd0\xbc\xd1\x8f')),
                ('second_name', models.CharField(max_length=250, verbose_name=b'\xd0\xa4\xd0\xb0\xd0\xbc\xd0\xb8\xd0\xbb\xd0\xb8\xd1\x8f')),
                ('hire_date', models.DateField(default=datetime.datetime.now, verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbd\xd0\xb0\xd0\xb5\xd0\xbc\xd0\xb0 (\xd0\x93\xd0\x93-\xd0\x9c\xd0\x9c-\xd0\x94\xd0\x94)')),
                ('department', models.ForeignKey(default=1, to='stafftime.Department')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeAttendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arriving_time', models.TimeField(verbose_name=b'\xd0\x92\xd1\x80\xd0\xb5\xd0\xbc\xd1\x8f \xd0\xbf\xd1\x80\xd0\xb8\xd1\x85\xd0\xbe\xd0\xb4\xd0\xb0')),
                ('leaving_time', models.TimeField(verbose_name=b'\xd0\x92\xd1\x80\xd0\xb5\xd0\xbc\xd1\x8f \xd1\x83\xd1\x85\xd0\xbe\xd0\xb4\xd0\xb0')),
                ('current_day', models.DateField(default=datetime.datetime.now, verbose_name=b'\xd0\x94\xd0\xb5\xd0\xbd\xd1\x8c (\xd0\x93\xd0\x93-\xd0\x9c\xd0\x9c-\xd0\x94\xd0\x94)')),
                ('employee', models.ForeignKey(default=1, to='stafftime.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='Timeline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('turn', models.CharField(max_length=128, verbose_name=b'\xd0\x92\xd0\xb8\xd0\xb4 \xd1\x81\xd0\xbc\xd0\xb5\xd0\xbd\xd1\x8b')),
                ('start_time', models.TimeField(verbose_name=b'\xd0\x92\xd1\x80\xd0\xb5\xd0\xbc\xd1\x8f \xd0\xbd\xd0\xb0\xd1\x87\xd0\xb0\xd0\xbb\xd0\xb0')),
                ('end_time', models.TimeField(verbose_name=b'\xd0\x92\xd1\x80\xd0\xb5\xd0\xbc\xd1\x8f \xd0\xb7\xd0\xb0\xd0\xb2\xd0\xb5\xd1\x80\xd1\x88\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f')),
                ('department', models.ForeignKey(default=1, to='stafftime.Department')),
            ],
        ),
    ]
