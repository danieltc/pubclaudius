# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-22 12:53
from __future__ import unicode_literals

from django.db import migrations, models
import rol.models


class Migration(migrations.Migration):

    dependencies = [
        ('rol', '0024_auto_20180122_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa',
            name='foto',
            field=models.ImageField(null=True, upload_to=rol.models.Pessoa.pic_pessoa_id),
        ),
    ]