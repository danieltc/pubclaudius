# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-26 13:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rol', '0025_auto_20180122_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='pessoa',
            name='tem_filhos',
            field=models.NullBooleanField(),
        ),
    ]