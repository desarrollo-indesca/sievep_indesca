# Generated by Django 4.2.4 on 2024-07-23 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calderas', '0027_salidafracciones_so2'),
    ]

    operations = [
        migrations.AddField(
            model_name='salidabalanceenergia',
            name='energia_total_salida',
            field=models.FloatField(default=100000000),
            preserve_default=False,
        ),
    ]
