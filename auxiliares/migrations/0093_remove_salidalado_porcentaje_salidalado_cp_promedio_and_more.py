# Generated by Django 4.2.4 on 2024-09-05 08:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auxiliares', '0092_rename_precalentador_evaluacionprecalentadoraire_equipo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salidalado',
            name='porcentaje',
        ),
        migrations.AddField(
            model_name='salidalado',
            name='cp_promedio',
            field=models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='salidalado',
            name='tipo',
            field=models.CharField(choices=[('E', 'Enrada'), ('S', 'Salida')], default=1, max_length=1, verbose_name='Tipo'),
            preserve_default=False,
        ),
    ]
