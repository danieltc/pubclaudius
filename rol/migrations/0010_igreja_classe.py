# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-21 13:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rol', '0009_auto_20171021_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='igreja',
            name='classe',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
