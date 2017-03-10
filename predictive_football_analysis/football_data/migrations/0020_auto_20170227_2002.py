# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-27 20:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football_data', '0019_auto_20170227_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='datafeature',
            name='display_name',
            field=models.CharField(default='', help_text='The readable name of this feature', max_length=40),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='datafeature',
            name='name',
            field=models.CharField(help_text='The name as it appears in the dataset', max_length=50),
        ),
    ]
