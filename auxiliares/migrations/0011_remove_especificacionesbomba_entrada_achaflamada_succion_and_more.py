# Generated by Django 4.2.4 on 2024-03-14 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auxiliares', '0010_especificacionesinstalacion_activo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='especificacionesbomba',
            name='entrada_achaflamada_succion',
        ),
        migrations.RemoveField(
            model_name='especificacionesbomba',
            name='entrada_bordes_afilados_succion',
        ),
        migrations.RemoveField(
            model_name='especificacionesbomba',
            name='entrada_proyectada_dentro_succion',
        ),
        migrations.RemoveField(
            model_name='especificacionesbomba',
            name='salida',
        ),
        migrations.RemoveField(
            model_name='especificacionesinstalacion',
            name='activo',
        ),
    ]
