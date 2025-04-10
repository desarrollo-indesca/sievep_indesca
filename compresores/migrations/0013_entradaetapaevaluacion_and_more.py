# Generated by Django 4.2.4 on 2025-03-13 08:28

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('intercambiadores', '0083_alter_evaluacionesintercambiador_ensuciamiento'),
        ('compresores', '0012_propiedadescompresor_tipo_lubricante'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntradaEtapaEvaluacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flujo_gas', models.FloatField(validators=[django.core.validators.MinValueValidator(1e-05)], verbose_name='Flujo de Gas')),
                ('flujo_volumetrico', models.FloatField(validators=[django.core.validators.MinValueValidator(1e-05)], verbose_name='Flujo Volumétrico')),
                ('flujo_surge', models.FloatField(validators=[django.core.validators.MinValueValidator(1e-05)], verbose_name='Flujo Surge / Aumento Estimado')),
                ('cabezal_politropico', models.FloatField(validators=[django.core.validators.MinValueValidator(1e-05)], verbose_name='Cabezal Politérpico')),
                ('potencia_generada', models.FloatField(validators=[django.core.validators.MinValueValidator(1e-05)], verbose_name='Potencia Generada')),
                ('eficiencia_politropica', models.FloatField(validators=[django.core.validators.MinValueValidator(1e-05)], verbose_name='Eficiencia Politérpica')),
                ('presion', models.FloatField(validators=[django.core.validators.MinValueValidator(1e-05)], verbose_name='Presión')),
                ('temperatura_in', models.FloatField(validators=[django.core.validators.MinValueValidator(1e-05)], verbose_name='Temperatura de Entrada')),
                ('temperatura_out', models.FloatField(validators=[django.core.validators.MinValueValidator(1e-05)], verbose_name='Temperatura de Salida')),
                ('k', models.FloatField(validators=[django.core.validators.MinValueValidator(1e-05)], verbose_name='Relación de Compresión')),
                ('z_in', models.FloatField(validators=[django.core.validators.MinValueValidator(1e-05)], verbose_name='Compresibilidad de Entrada')),
                ('z_out', models.FloatField(validators=[django.core.validators.MinValueValidator(1e-05)], verbose_name='Compresibilidad de Salida')),
                ('pm_ficha', models.FloatField(validators=[django.core.validators.MinValueValidator(1e-05)], verbose_name='Potencia Máxima')),
                ('cabezal_politropico_unidad', models.ForeignKey(blank=True, default=7, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='unidad_cabezal_politropico_evaluacion', to='intercambiadores.unidades', verbose_name='Unidad')),
            ],
        ),
        migrations.AlterField(
            model_name='etapacompresor',
            name='aumento_estimado',
            field=models.FloatField(blank=True, null=True, verbose_name='Aumento Estimado / Flujo Surge'),
        ),
        migrations.AlterField(
            model_name='ladoetapacompresor',
            name='lado',
            field=models.CharField(choices=[('E', 'Entrada'), ('S', 'Salida')], max_length=1, verbose_name='Lado del Compresor'),
        ),
        migrations.CreateModel(
            name='SalidaEtapaEvaluacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flujo_in', models.FloatField()),
                ('flujo_out', models.FloatField()),
                ('cabezal_calculado', models.FloatField()),
                ('cabezal_isotropico', models.FloatField()),
                ('potencia_calculada', models.FloatField()),
                ('potencia_isoentropica', models.FloatField()),
                ('eficiencia_iso', models.FloatField()),
                ('eficiencia_teorica', models.FloatField()),
                ('caida_presion', models.FloatField()),
                ('caida_temp', models.FloatField()),
                ('k_calculada', models.FloatField()),
                ('k_promedio', models.FloatField()),
                ('n', models.FloatField()),
                ('z_in', models.FloatField()),
                ('z_out', models.FloatField()),
                ('relacion_compresion', models.FloatField()),
                ('relacion_temperatura', models.FloatField()),
                ('relacion_volumetrica', models.FloatField()),
                ('entrada_etapa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salidas', to='compresores.entradaetapaevaluacion')),
            ],
        ),
        migrations.AddField(
            model_name='entradaetapaevaluacion',
            name='etapa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entradas', to='compresores.etapacompresor'),
        ),
        migrations.AddField(
            model_name='entradaetapaevaluacion',
            name='evaluacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entradas_evaluacion', to='compresores.evaluacion'),
        ),
        migrations.AddField(
            model_name='entradaetapaevaluacion',
            name='flujo_gas_unidad',
            field=models.ForeignKey(blank=True, default=54, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='unidad_flujo_gas_evaluacion', to='intercambiadores.unidades', verbose_name='Unidad'),
        ),
        migrations.AddField(
            model_name='entradaetapaevaluacion',
            name='flujo_volumetrico_unidad',
            field=models.ForeignKey(blank=True, default=94, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='unidad_flujo_volumetrico_evaluacion', to='intercambiadores.unidades', verbose_name='Unidad'),
        ),
        migrations.AddField(
            model_name='entradaetapaevaluacion',
            name='pm_ficha_unidad',
            field=models.ForeignKey(blank=True, default=2, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='unidad_pm_ficha_evaluacion', to='intercambiadores.unidades', verbose_name='Unidad'),
        ),
        migrations.AddField(
            model_name='entradaetapaevaluacion',
            name='potencia_generada_unidad',
            field=models.ForeignKey(blank=True, default=2, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='unidad_potencia_generada_evaluacion', to='intercambiadores.unidades', verbose_name='Unidad'),
        ),
        migrations.AddField(
            model_name='entradaetapaevaluacion',
            name='presion_unidad',
            field=models.ForeignKey(blank=True, default=7, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='unidad_presion_evaluacion', to='intercambiadores.unidades', verbose_name='Unidad'),
        ),
        migrations.AddField(
            model_name='entradaetapaevaluacion',
            name='temperatura_unidad',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='unidad_temperatura_out_evaluacion', to='intercambiadores.unidades', verbose_name='Unidad'),
        ),
        migrations.CreateModel(
            name='ComposicionEvaluacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('porc_molar', models.FloatField(validators=[django.core.validators.MinValueValidator(1e-05)], verbose_name='Porcentaje')),
                ('entrada_etapa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='composiciones', to='compresores.entradaetapaevaluacion')),
                ('fluido', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='composiciones_fluidos', to='intercambiadores.fluido')),
            ],
        ),
    ]
