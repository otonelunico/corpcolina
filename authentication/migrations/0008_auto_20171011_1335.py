# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-11 16:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_auto_20170907_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='logeado',
            name='admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='logeado',
            name='docs',
            field=models.BooleanField(default=False),
        ),
    ]