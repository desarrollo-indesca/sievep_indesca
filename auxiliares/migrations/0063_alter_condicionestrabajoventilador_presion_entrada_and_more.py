# Generated by Django 4.2.4 on 2024-05-27 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auxiliares', '0062_alter_bombas_grafica_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condicionestrabajoventilador',
            name='presion_entrada',
            field=models.FloatField(blank=True, null=True, verbose_name='Presión de Entrada'),
        ),
        migrations.AlterField(
            model_name='condicionestrabajoventilador',
            name='presion_salida',
            field=models.FloatField(blank=True, null=True, verbose_name='Presión de Salida'),
        ),
        migrations.AlterField(
            model_name='entradaevaluacionventilador',
            name='presion_entrada',
            field=models.FloatField(verbose_name='Presión Entrada'),
        ),
        migrations.AlterField(
            model_name='entradaevaluacionventilador',
            name='presion_salida',
            field=models.FloatField(verbose_name='Presión Salida'),
        ),
    ]
