# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-07 18:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_auto_20170907_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logeado',
            name='departament',
            field=models.CharField(max_length=30),
        ),
    ]
