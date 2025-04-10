# Generated by Django 4.2.4 on 2024-08-15 17:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('intercambiadores', '0073_intercambiador_copia'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auxiliares', '0072_alter_evaluacionventilador_equipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorrientePrecalentadorAgua',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
                ('numero_corriente', models.CharField(max_length=25)),
                ('flujo', models.FloatField()),
                ('presion', models.FloatField()),
                ('temperatura', models.FloatField()),
                ('entalpia', models.FloatField()),
                ('densidad', models.FloatField()),
                ('fase', models.CharField(choices=[('L', 'Líquido'), ('V', 'Vapor'), ('S', 'Saturado')], max_length=1)),
                ('lado', models.CharField(choices=[('C', 'Carcasa'), ('T', 'Tubos')], max_length=1)),
                ('rol', models.CharField(choices=[('E', 'Entrada'), ('S', 'Salida')], max_length=1)),
            ],
            options={
                'db_table': 'precalentador_agua_corriente',
                'ordering': ('rol',),
            },
        ),
        migrations.CreateModel(
            name='SalidaGeneralPrecalentadorAgua',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('mtd', models.FloatField()),
                ('factor_ensuciamiento', models.FloatField()),
                ('cmin', models.FloatField()),
                ('ntu', models.FloatField()),
                ('u', models.FloatField()),
                ('u_diseno', models.FloatField()),
                ('calor_carcasa', models.FloatField()),
                ('calor_tubos', models.FloatField()),
                ('eficiencia', models.FloatField()),
                ('calor_unidad', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='calor_unidad_evaluacion_precalentador_agua', to='intercambiadores.unidades')),
                ('cmin_unidad', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cmin_unidad_evaluacion_precalentador_agua', to='intercambiadores.unidades')),
                ('factor_ensuciamiento_unidad', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='factor_ensuciamiento_unidad_evaluacion_precalentador_agua', to='intercambiadores.unidades')),
                ('mtd_unidad', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='mtd_unidad_evaluacion_precalentador_agua', to='intercambiadores.unidades')),
                ('u_unidad', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='u_unidad_evaluacion_precalentador_agua', to='intercambiadores.unidades')),
            ],
            options={
                'db_table': 'precalentador_agua_evaluacion_salida_general',
            },
        ),
        migrations.CreateModel(
            name='EvaluacionPrecalentadorAgua',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('fecha', models.DateTimeField(auto_now=True)),
                ('precalentador', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='evaluacion_precalentador', to='auxiliares.precalentadoragua')),
                ('salida_general', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='auxiliares.salidageneralprecalentadoragua')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='evaluacion_precalentador', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'precalentador_agua_evaluacion',
            },
        ),
        migrations.CreateModel(
            name='CorrientesEvaluacionPrecalentadorAgua',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('flujo', models.FloatField()),
                ('presion', models.FloatField()),
                ('temperatura', models.FloatField()),
                ('entalpia', models.FloatField()),
                ('densidad', models.FloatField()),
                ('fase', models.CharField(choices=[('L', 'Líquido'), ('V', 'Vapor'), ('S', 'Saturado')], max_length=1)),
                ('corriente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='corrientes_evaluacion_precalentador_agua', to='auxiliares.corrienteprecalentadoragua')),
            ],
            options={
                'db_table': 'precalentador_agua_evaluacion_corriente',
            },
        ),
    ]
