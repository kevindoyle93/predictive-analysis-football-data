# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-28 12:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football_data', '0024_auto_20170228_0022'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingDrill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('description', models.TextField()),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='training_drills', to='football_data.DataFeature')),
                ('sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='training_drills', to='football_data.Sport')),
            ],
        ),
    ]