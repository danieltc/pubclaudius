# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-20 23:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rol', '0006_auto_20171020_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa',
            name='nome',
            field=models.CharField(max_length=128, null=True),
        ),
    ]