# Generated by Django 4.2.4 on 2025-03-27 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compresores', '0018_salidaetapaevaluacion_caida_presion_unidad_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salidaetapaevaluacion',
            name='caida_presion_unidad',
        ),
        migrations.RemoveField(
            model_name='salidaetapaevaluacion',
            name='caida_temp_unidad',
        ),
    ]
