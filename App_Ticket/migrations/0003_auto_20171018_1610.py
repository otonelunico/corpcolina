# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-18 19:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Ticket', '0002_remove_tecnico_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='celu_contacto',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='fijo_contacto',
            field=models.IntegerField(blank=True),
        ),
    ]
