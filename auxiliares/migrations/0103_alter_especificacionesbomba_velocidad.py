# Generated by Django 4.2.4 on 2024-10-21 10:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auxiliares', '0102_alter_especificacionesbomba_numero_etapas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='especificacionesbomba',
            name='velocidad',
            field=models.FloatField(default=100, validators=[django.core.validators.MinValueValidator(0.0001)]),
            preserve_default=False,
        ),
    ]
