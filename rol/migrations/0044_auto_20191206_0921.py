# Generated by Django 2.0 on 2019-12-06 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rol', '0043_merge_20191112_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='turmafrequencia',
            name='restrito',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='relatorio',
            name='invalido',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='relatorio',
            name='rol_separado',
            field=models.NullBooleanField(default=False),
        ),
    ]
