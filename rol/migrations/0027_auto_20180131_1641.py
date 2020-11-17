# Generated by Django 2.0 on 2018-01-31 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rol', '0026_pessoa_tem_filhos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agregadorcategoria',
            name='descricao',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='ata',
            name='identificacao',
            field=models.CharField(max_length=256, unique=True),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='descricao',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='detalhes',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='contato',
            name='conteudo',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='igreja',
            name='cidade',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='igreja',
            name='classe',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='igreja',
            name='email_secretario_conselho',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='igreja',
            name='nome',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='igreja',
            name='nome_secretario_conselho',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='oficialato',
            name='cargo',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='oficialato',
            name='ordenacao',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='apelido',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='batismo_onde',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='batismo_quando',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='nome',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='nome_ascii',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='profissao_fe_onde',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='profissao_fe_quando',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='tipoadmissao',
            name='descricao',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='tipoato',
            name='descricao',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='tipoato',
            name='detalhes',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='tipocontato',
            name='desc_legado',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='tipocontato',
            name='desc_sistema',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='tipocontato',
            name='descricao',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='tipocontato',
            name='detalhes',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='tipodemissao',
            name='descricao',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='tipoestadocivil',
            name='descricao',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='tipoestadocivil',
            name='detalhes',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
