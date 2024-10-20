# Generated by Django 4.2.4 on 2024-06-17 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('intercambiadores', '0070_alter_evaluacionesintercambiador_id'),
        ('calderas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Caracteristica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clase', models.CharField(max_length=1)),
                ('nombre', models.CharField(max_length=45)),
                ('tipo_unidad', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Combustible',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_gas', models.CharField(max_length=45)),
                ('liquido', models.BooleanField()),
                ('nombre_liquido', models.CharField(blank=True, max_length=45, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DimsSobrecalentador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_total_transferencia', models.FloatField(blank=True, null=True)),
                ('diametro_tubos', models.FloatField(blank=True, null=True)),
                ('num_tubos', models.IntegerField(blank=True, null=True)),
                ('area_unidad', models.ForeignKey(default=3, on_delete=django.db.models.deletion.PROTECT, related_name='area_unidad_sobrecalentador', to='intercambiadores.unidades')),
                ('diametro_unidad', models.ForeignKey(default=4, on_delete=django.db.models.deletion.PROTECT, related_name='diametro_unidad_sobrecalentador', to='intercambiadores.unidades')),
            ],
        ),
        migrations.CreateModel(
            name='SalidaBalanceMolar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n_gas_entrada', models.FloatField()),
                ('n_aire_gas_entrada', models.FloatField()),
                ('n_total', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SalidaFracciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('h2o', models.FloatField()),
                ('co2', models.FloatField()),
                ('n2', models.FloatField()),
                ('so2', models.FloatField()),
                ('o2', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='caldera',
            name='accesorios',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
        migrations.AddField(
            model_name='caldera',
            name='tipo_caldera',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
        migrations.AlterModelTable(
            name='caldera',
            table=None,
        ),
        migrations.CreateModel(
            name='ValorPorCarga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=1)),
                ('carga', models.FloatField()),
                ('valor_num', models.FloatField()),
                ('caracteristica', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='calderas.caracteristica')),
                ('unidad', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='intercambiadores.unidades')),
            ],
        ),
        migrations.CreateModel(
            name='Tambor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('presion_operacion', models.FloatField(blank=True, null=True)),
                ('temp_operacion', models.FloatField(blank=True, null=True)),
                ('presion_diseno', models.FloatField(blank=True, null=True)),
                ('temp_diseno', models.FloatField(blank=True, null=True)),
                ('material', models.CharField(blank=True, max_length=45, null=True)),
                ('presion_unidad', models.ForeignKey(default=33, on_delete=django.db.models.deletion.PROTECT, related_name='presion_unidad_tambor', to='intercambiadores.unidades')),
                ('temperatura_unidad', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='temperatura_unidad_tambor', to='intercambiadores.unidades')),
            ],
        ),
        migrations.CreateModel(
            name='Sobrecalentador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('presion_operacion', models.FloatField()),
                ('temp_operacion', models.FloatField()),
                ('presion_diseno', models.FloatField()),
                ('flujo_max_continuo', models.FloatField()),
                ('dims', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='calderas.dimssobrecalentador')),
                ('flujo_unidad', models.ForeignKey(default=26, on_delete=django.db.models.deletion.PROTECT, related_name='flujo_unidad_sobrecalentador', to='intercambiadores.unidades')),
                ('presion_unidad', models.ForeignKey(default=33, on_delete=django.db.models.deletion.PROTECT, related_name='presion_unidad_sobrecalentador', to='intercambiadores.unidades')),
                ('temperatura_unidad', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='temperatura_unidad_sobrecalentador', to='intercambiadores.unidades')),
            ],
        ),
        migrations.CreateModel(
            name='SeccionTambor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seccion', models.CharField(choices=[('I', 'Inferior'), ('S', 'Superior')], max_length=1)),
                ('diametro', models.FloatField(blank=True, null=True)),
                ('longitud', models.FloatField(blank=True, null=True)),
                ('dimensiones_unidad', models.ForeignKey(default=4, on_delete=django.db.models.deletion.PROTECT, to='intercambiadores.unidades')),
                ('tambor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='calderas.tambor')),
            ],
        ),
        migrations.CreateModel(
            name='SalidaLadoAgua',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flujo_purga', models.FloatField()),
                ('energia_vapor', models.FloatField()),
                ('eficiencia', models.FloatField()),
                ('flujo_unidad', models.ForeignKey(default=3, on_delete=django.db.models.deletion.PROTECT, related_name='flujo_salida_agua_evaluacion', to='intercambiadores.unidades')),
            ],
        ),
        migrations.CreateModel(
            name='SalidaFlujosEntrada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flujo_gas_entrada', models.FloatField()),
                ('flujo_aire_entrada', models.FloatField()),
                ('flujo_combustion', models.FloatField()),
                ('flujo_combustion_vol', models.FloatField()),
                ('porc_o2_exceso', models.FloatField()),
                ('flujo_masico_unidad', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='flujo_masico_unidad_salida_flujos_evaluacion', to='intercambiadores.unidades')),
                ('flujo_vol_unidad', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='flujo_volumetrico_unidad_salida_flujos_evaluacion', to='intercambiadores.unidades')),
            ],
        ),
        migrations.CreateModel(
            name='SalidaBalanceEnergia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('energia_entrada_gas', models.FloatField()),
                ('energia_entrada_aire', models.FloatField()),
                ('energia_total_entrada', models.FloatField()),
                ('energia_total_reaccion', models.FloatField()),
                ('energia_horno', models.FloatField()),
                ('energia_unidad', models.ForeignKey(default=4, on_delete=django.db.models.deletion.PROTECT, related_name='energia_salida_agua_evaluacion', to='intercambiadores.unidades')),
            ],
        ),
        migrations.CreateModel(
            name='Evaluacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_created=True)),
                ('nombre', models.CharField(max_length=45)),
                ('caldera', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='calderas.caldera')),
                ('salida_balance_energia', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='calderas.salidabalanceenergia')),
                ('salida_balance_molar', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='calderas.salidabalancemolar')),
                ('salida_flujos', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='calderas.salidaflujosentrada')),
                ('salida_fracciones', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='calderas.salidafracciones')),
                ('salida_lado_agua', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='calderas.salidaladoagua')),
            ],
        ),
        migrations.CreateModel(
            name='EspecificacionesCaldera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.CharField(blank=True, max_length=45, null=True)),
                ('area_transferencia_calor', models.FloatField(blank=True, null=True)),
                ('calor_intercambiado', models.FloatField(blank=True, null=True)),
                ('capacidad', models.FloatField(blank=True, null=True)),
                ('temp_diseno', models.FloatField(blank=True, null=True)),
                ('temp_operacion', models.FloatField(blank=True, null=True)),
                ('presion_diseno', models.FloatField(blank=True, null=True)),
                ('presion_operacion', models.FloatField(blank=True, null=True)),
                ('carga', models.FloatField(blank=True, null=True)),
                ('eficiencia_termica', models.FloatField(blank=True, null=True)),
                ('area_unidad', models.ForeignKey(default=3, on_delete=django.db.models.deletion.PROTECT, related_name='area_unidad_especificaciones', to='intercambiadores.unidades')),
                ('calor_unidad', models.ForeignKey(default=62, on_delete=django.db.models.deletion.PROTECT, related_name='calor_unidad_especificaciones', to='intercambiadores.unidades')),
                ('capacidad_unidad', models.ForeignKey(default=6, on_delete=django.db.models.deletion.PROTECT, related_name='capacidad_unidad_especificaciones', to='intercambiadores.unidades')),
                ('carga_unidad', models.ForeignKey(default=6, on_delete=django.db.models.deletion.PROTECT, related_name='carga_unidad_especificaciones', to='intercambiadores.unidades')),
                ('presion_unidad', models.ForeignKey(default=33, on_delete=django.db.models.deletion.PROTECT, related_name='presion_unidad_especificaciones', to='intercambiadores.unidades')),
                ('temperatura_unidad', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='temperatura_unidad_especificaciones', to='intercambiadores.unidades')),
            ],
        ),
        migrations.CreateModel(
            name='EntradasFluidos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_fluido', models.CharField(max_length=45, verbose_name='Nombre del Fluido')),
                ('flujo', models.FloatField(verbose_name='Flujo Másico')),
                ('temperatura', models.FloatField(verbose_name='Temperatura de Operación')),
                ('presion', models.FloatField(verbose_name='Presión de Operación')),
                ('tipo_fluido', models.CharField(choices=[('G', 'Gas'), ('A', 'Aire'), ('H', 'Horno'), ('L', 'Líquido'), ('W', 'Agua de Entrada a la Caldera'), ('V', 'Vapor Producido')], max_length=1)),
                ('humedad_relativa', models.FloatField(blank=True, null=True)),
                ('evaluacion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='calderas.evaluacion')),
            ],
        ),
        migrations.CreateModel(
            name='Economizador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_total_transferencia', models.FloatField(blank=True, null=True)),
                ('diametro_tubos', models.FloatField(blank=True, null=True)),
                ('numero_tubos', models.IntegerField(null=True)),
                ('area_unidad', models.ForeignKey(default=3, on_delete=django.db.models.deletion.PROTECT, related_name='area_unidad_economizador', to='intercambiadores.unidades')),
                ('diametro_unidad', models.ForeignKey(default=4, on_delete=django.db.models.deletion.PROTECT, related_name='diametro_unidad_economizador', to='intercambiadores.unidades')),
            ],
        ),
        migrations.CreateModel(
            name='DimensionesCaldera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ancho', models.FloatField()),
                ('largo', models.FloatField()),
                ('alto', models.FloatField()),
                ('dimensiones_unidad', models.ForeignKey(default=4, on_delete=django.db.models.deletion.PROTECT, to='intercambiadores.unidades')),
            ],
        ),
        migrations.CreateModel(
            name='Corriente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=45, unique=True)),
                ('tipo', models.CharField(choices=[('V', 'Vapor de Alta Presión'), ('A', 'Agua'), ('P', 'Purga'), ('V', 'Vapor de Baja Presión')], max_length=1)),
                ('flujo_masico', models.FloatField()),
                ('densidad', models.FloatField()),
                ('estado', models.CharField(choices=[('L', 'Líquido'), ('V', 'Vapor')], max_length=1)),
                ('temp_operacion', models.FloatField()),
                ('presion', models.FloatField()),
                ('caldera', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='calderas.caldera')),
                ('densidad_unidad', models.ForeignKey(default=43, on_delete=django.db.models.deletion.PROTECT, related_name='densidad_unidad_corriente_corriente_calderas', to='intercambiadores.unidades')),
                ('flujo_masico_unidad', models.ForeignKey(default=26, on_delete=django.db.models.deletion.PROTECT, related_name='flujomasico_unidad_corriente_calderas', to='intercambiadores.unidades')),
                ('presion_unidad', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='presion_unidad_corriente_calderas', to='intercambiadores.unidades')),
                ('temp_operacion_unidad', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='temp_operacion_unidad_corriente_calderas', to='intercambiadores.unidades')),
            ],
        ),
        migrations.CreateModel(
            name='ComposicionCombustible',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('porc_vol', models.FloatField()),
                ('porc_aire', models.FloatField()),
                ('combustible', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='calderas.combustible')),
                ('fluido', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='intercambiadores.fluido')),
            ],
        ),
        migrations.CreateModel(
            name='Chimenea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diametro', models.FloatField(blank=True, null=True)),
                ('altura', models.FloatField(blank=True, null=True)),
                ('dimensiones_unidad', models.ForeignKey(default=4, on_delete=django.db.models.deletion.PROTECT, to='intercambiadores.unidades')),
            ],
        ),
        migrations.AddField(
            model_name='caracteristica',
            name='caldera',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='calderas.caldera'),
        ),
        migrations.AddField(
            model_name='caldera',
            name='chimenea',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.PROTECT, to='calderas.chimenea'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='caldera',
            name='combustible',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.PROTECT, to='calderas.combustible'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='caldera',
            name='dimensiones',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.PROTECT, to='calderas.dimssobrecalentador'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='caldera',
            name='economizador',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.PROTECT, to='calderas.economizador'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='caldera',
            name='especificaciones',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.PROTECT, to='calderas.especificacionescaldera'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='caldera',
            name='sobrecalentador',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='calderas.sobrecalentador'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='caldera',
            name='tambor',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.PROTECT, to='calderas.tambor'),
            preserve_default=False,
        ),
    ]
