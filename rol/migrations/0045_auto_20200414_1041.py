# Generated by Django 2.0 on 2020-04-14 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rol', '0044_auto_20191206_0921'),
    ]

    operations = [
        migrations.AddField(
            model_name='relatorio',
            name='chefe_familia',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='relatorio',
            name='campo1',
            field=models.CharField(choices=[('nome', 'Nome'), ('foto', 'Foto'), ('sexo', 'Sexo'), ('comungante', 'Membro Comungante'), ('categoria', 'Categoria'), ('idade', 'Idade'), ('data_nascimento', 'Aniversário'), ('data_falecimento', 'Data de Falecimento'), ('forma_admissao_pretendida', 'Forma de Admissão Pretendida'), ('estado_civil', 'Estado Civil'), ('estado_civil_complemento', 'Namoro e Noivado'), ('data_inicio_relacionamento', 'Aniversário do Relacionamento'), ('data_pedido_admissao', 'Data do Pedido de Admissao'), ('tem_filhos', 'Tem Filho[s]'), ('rol', 'Rol'), ('forma_admissao', 'Forma de Admissão'), ('data_admissao', 'Data de Admissão'), ('forma_demissao', 'Forma de Demissão'), ('data_demissao', 'Data de Demissão'), ('celular', 'Celular'), ('email', 'Email'), ('endereco', 'Endereço')], max_length=50),
        ),
        migrations.AlterField(
            model_name='relatorio',
            name='campo2',
            field=models.CharField(blank=True, choices=[('nome', 'Nome'), ('foto', 'Foto'), ('sexo', 'Sexo'), ('comungante', 'Membro Comungante'), ('categoria', 'Categoria'), ('idade', 'Idade'), ('data_nascimento', 'Aniversário'), ('data_falecimento', 'Data de Falecimento'), ('forma_admissao_pretendida', 'Forma de Admissão Pretendida'), ('estado_civil', 'Estado Civil'), ('estado_civil_complemento', 'Namoro e Noivado'), ('data_inicio_relacionamento', 'Aniversário do Relacionamento'), ('data_pedido_admissao', 'Data do Pedido de Admissao'), ('tem_filhos', 'Tem Filho[s]'), ('rol', 'Rol'), ('forma_admissao', 'Forma de Admissão'), ('data_admissao', 'Data de Admissão'), ('forma_demissao', 'Forma de Demissão'), ('data_demissao', 'Data de Demissão'), ('celular', 'Celular'), ('email', 'Email'), ('endereco', 'Endereço')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='relatorio',
            name='campo3',
            field=models.CharField(blank=True, choices=[('nome', 'Nome'), ('foto', 'Foto'), ('sexo', 'Sexo'), ('comungante', 'Membro Comungante'), ('categoria', 'Categoria'), ('idade', 'Idade'), ('data_nascimento', 'Aniversário'), ('data_falecimento', 'Data de Falecimento'), ('forma_admissao_pretendida', 'Forma de Admissão Pretendida'), ('estado_civil', 'Estado Civil'), ('estado_civil_complemento', 'Namoro e Noivado'), ('data_inicio_relacionamento', 'Aniversário do Relacionamento'), ('data_pedido_admissao', 'Data do Pedido de Admissao'), ('tem_filhos', 'Tem Filho[s]'), ('rol', 'Rol'), ('forma_admissao', 'Forma de Admissão'), ('data_admissao', 'Data de Admissão'), ('forma_demissao', 'Forma de Demissão'), ('data_demissao', 'Data de Demissão'), ('celular', 'Celular'), ('email', 'Email'), ('endereco', 'Endereço')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='relatorio',
            name='campo4',
            field=models.CharField(blank=True, choices=[('nome', 'Nome'), ('foto', 'Foto'), ('sexo', 'Sexo'), ('comungante', 'Membro Comungante'), ('categoria', 'Categoria'), ('idade', 'Idade'), ('data_nascimento', 'Aniversário'), ('data_falecimento', 'Data de Falecimento'), ('forma_admissao_pretendida', 'Forma de Admissão Pretendida'), ('estado_civil', 'Estado Civil'), ('estado_civil_complemento', 'Namoro e Noivado'), ('data_inicio_relacionamento', 'Aniversário do Relacionamento'), ('data_pedido_admissao', 'Data do Pedido de Admissao'), ('tem_filhos', 'Tem Filho[s]'), ('rol', 'Rol'), ('forma_admissao', 'Forma de Admissão'), ('data_admissao', 'Data de Admissão'), ('forma_demissao', 'Forma de Demissão'), ('data_demissao', 'Data de Demissão'), ('celular', 'Celular'), ('email', 'Email'), ('endereco', 'Endereço')], max_length=50, null=True),
        ),
    ]
