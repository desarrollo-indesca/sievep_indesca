# Generated by Django 4.2.4 on 2024-05-27 09:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turbinas', '0011_alter_corrienteevaluacion_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entradacorriente',
            name='presion',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0001)]),
        ),
    ]
