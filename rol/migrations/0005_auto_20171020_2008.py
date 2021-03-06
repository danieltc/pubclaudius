# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-20 22:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rol', '0004_auto_20171007_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa',
            name='apelido',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='batismo_onde',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='batismo_quando',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='categoria',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pessoas', to='rol.Categoria'),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='chefe_familia',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='membros_da_familia', to='rol.Pessoa'),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='conjuge',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pessoa_conjuge', to='rol.Pessoa'),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='cpf',
            field=models.CharField(max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='data_nascimento',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='data_pedido_admissao',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='estado_civil',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pessoas', to='rol.TipoEstadoCivil'),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='forma_admissao_pretendida',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pessoas', to='rol.TipoAdmissao'),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='foto',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='igreja_origem',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pessoas', to='rol.Igreja'),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='mae',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='filhos_m', to='rol.Pessoa'),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='observacoes_legado',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='pai',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='filhos_p', to='rol.Pessoa'),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='profissao_fe_onde',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='profissao_fe_quando',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='razoes_pedido_admissao',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='rg',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
