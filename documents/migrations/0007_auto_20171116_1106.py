# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-16 14:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0006_auto_20171116_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='body',
            field=models.TextField(blank=True, default='NA'),
        ),
    ]