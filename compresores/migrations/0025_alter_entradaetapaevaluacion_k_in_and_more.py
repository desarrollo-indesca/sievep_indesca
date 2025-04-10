# Generated by Django 4.2.4 on 2025-04-08 14:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compresores', '0024_remove_propiedadescompresor_pm_etapacompresor_pm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entradaetapaevaluacion',
            name='k_in',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1e-05)], verbose_name='Relación de Compresión'),
        ),
        migrations.AlterField(
            model_name='entradaetapaevaluacion',
            name='k_out',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1e-05)], verbose_name='Relación de Compresión'),
        ),
        migrations.AlterField(
            model_name='entradaetapaevaluacion',
            name='potencia_generada',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1e-05)], verbose_name='Potencia Generada'),
        ),
        migrations.AlterField(
            model_name='entradaetapaevaluacion',
            name='z_in',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1e-05)], verbose_name='Compresibilidad de Entrada'),
        ),
        migrations.AlterField(
            model_name='entradaetapaevaluacion',
            name='z_out',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1e-05)], verbose_name='Compresibilidad de Salida'),
        ),
        migrations.AlterField(
            model_name='etapacompresor',
            name='eficiencia_isentropica',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)], verbose_name='Eficiencia Isoentrópica'),
        ),
        migrations.AlterField(
            model_name='etapacompresor',
            name='nombre_fluido',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='Nombre del Gas'),
        ),
        migrations.AlterField(
            model_name='propiedadescompresor',
            name='potencia_requerida',
            field=models.FloatField(blank=True, null=True, verbose_name='Potencia Requerida Total'),
        ),
    ]
