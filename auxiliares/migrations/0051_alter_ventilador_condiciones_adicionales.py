# Generated by Django 4.2.4 on 2024-04-23 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auxiliares', '0050_condicionestrabajoventilador_potencia_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ventilador',
            name='condiciones_adicionales',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='condicion_trabajo_adicional_ventilador', to='auxiliares.condicionestrabajoventilador'),
        ),
    ]
