# Generated by Django 2.0 on 2018-03-12 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rol', '0036_auto_20180312_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turmafrequencia',
            name='tipo',
            field=models.CharField(choices=[('culto', 'Culto'), ('bercario', 'Berçário'), ('ebd', 'Escola Bíblica Dominical'), ('ebdi', 'Escola Bíblica Dominical Infantil'), ('gf', 'Grupos Familiares'), ('si', 'Sociedades Internas'), ('outro', 'Outros Eventos')], max_length=8),
        ),
    ]
