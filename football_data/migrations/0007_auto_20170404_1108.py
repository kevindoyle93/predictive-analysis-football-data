# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-04 11:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('football_data', '0006_auto_20170402_1030'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainedModels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trained_model', picklefield.fields.PickledObjectField(editable=False)),
            ],
        ),
        migrations.AddField(
            model_name='machinelearningmodel',
            name='pickled_model',
            field=picklefield.fields.PickledObjectField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='trainedmodels',
            name='ml_algorithm',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='trained_model', to='football_data.MachineLearningModel'),
        ),
    ]
