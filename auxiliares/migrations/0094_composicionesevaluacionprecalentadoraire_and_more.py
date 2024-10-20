# Generated by Django 4.2.4 on 2024-09-05 13:21

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('intercambiadores', '0073_intercambiador_copia'),
        ('auxiliares', '0093_remove_salidalado_porcentaje_salidalado_cp_promedio_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComposicionesEvaluacionPrecalentadorAire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('porcentaje', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('entrada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='composicion_combustible', to='auxiliares.entradalado')),
                ('fluido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='composicion_combustible', to='intercambiadores.fluido')),
            ],
            options={
                'db_table': 'precalentador_aire_evaluacion_composiciones',
            },
        ),
        migrations.DeleteModel(
            name='SalidaLado',
        ),
    ]
