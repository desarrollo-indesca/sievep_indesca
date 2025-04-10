# Generated by Django 4.2.4 on 2024-08-13 08:39

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calderas', '0032_entradasfluidos_area_entradasfluidos_area_unidad_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PerdidasIndirecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('perdidas_gas_secos', models.FloatField()),
                ('perdidas_humedad_combustible', models.FloatField()),
                ('perdidas_humedad_aire', models.FloatField()),
                ('perdidas_h2', models.FloatField()),
                ('perdidas_radiacion_conveccion', models.FloatField()),
            ],
        ),
        migrations.AlterField(
            model_name='entradasfluidos',
            name='area',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0001)], verbose_name='Área'),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='equipo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='equipo_evaluacion_caldera', to='calderas.caldera'),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='metodo',
            field=models.CharField(choices=[('D', 'Directo'), ('I', 'Indirecto')], max_length=1, verbose_name='Método'),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='salida_balance_energia',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='calderas.salidabalanceenergia'),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='salida_flujos',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='calderas.salidaflujosentrada'),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='salida_fracciones',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='calderas.salidafracciones'),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='salida_lado_agua',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='calderas.salidaladoagua'),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='perdidas_indirecto',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='calderas.perdidasindirecto'),
        ),
    ]
