# Generated by Django 4.2.4 on 2024-07-15 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calderas', '0024_remove_entradacomposicion_normalizado_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entradasfluidos',
            options={'ordering': ('tipo_fluido',)},
        ),
        migrations.RemoveField(
            model_name='evaluacion',
            name='salida_balances',
        ),
        migrations.DeleteModel(
            name='SalidaBalances',
        ),
    ]
