# Generated by Django 2.0 on 2020-10-19 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rol', '0047_auto_20201008_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='oficialato',
            name='ativo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='oficialato',
            name='cargo_atual',
            field=models.CharField(choices=[('diacono', 'Diácono'), ('diacono_disp', 'Diácono em disponibilidade'), ('pastor_aux', 'Pastor Auxiliar'), ('pastor_evang', 'Pastor Evangelista'), ('pastor_titular', 'Pastor Titular'), ('presbitero', 'Presbítero'), ('presbitero_disp', 'Presbítero em disponibilidade'), ('presb_diac_disp', 'Presbítero/Diácono em disponibilidade')], default='-', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='oficialato',
            name='ordenacao_historico',
            field=models.CharField(choices=[('diaconato', 'Diaconato'), ('diaconato_presbiterato', 'Diaconato e Presbiterato'), ('diaconato_pastorado', 'Diaconato e Pastorado'), ('diaconato_presbiterato_pastorado', 'Diaconato, Presbiterato e Pastorado'), ('pastorado', 'Pastorado'), ('presbiterato', 'Presbiterato'), ('presbiterato_pastorado', 'Presbiterato e Pastorado')], default='-', max_length=256),
            preserve_default=False,
        ),
    ]
