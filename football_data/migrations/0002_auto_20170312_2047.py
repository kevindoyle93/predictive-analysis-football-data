# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-12 20:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football_data', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appmatch',
            name='coach',
        ),
        migrations.DeleteModel(
            name='AppMatch',
        ),
    ]