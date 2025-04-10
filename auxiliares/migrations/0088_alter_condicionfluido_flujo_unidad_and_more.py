# Generated by Django 4.2.4 on 2024-08-28 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('intercambiadores', '0073_intercambiador_copia'),
        ('auxiliares', '0087_entradalado_especificacionesprecalentadoraire_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condicionfluido',
            name='flujo_unidad',
            field=models.ForeignKey(default=6, on_delete=django.db.models.deletion.CASCADE, related_name='condicion_fluido_flujo_unidad', to='intercambiadores.unidades'),
        ),
        migrations.AlterField(
            model_name='condicionfluido',
            name='presion_unidad',
            field=models.ForeignKey(default=33, on_delete=django.db.models.deletion.CASCADE, related_name='condicion_fluido_presion_unidad', to='intercambiadores.unidades'),
        ),
        migrations.AlterField(
            model_name='condicionfluido',
            name='temp_unidad',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='condicion_fluido_temp_unidad', to='intercambiadores.unidades'),
        ),
        migrations.AlterField(
            model_name='especificacionesprecalentadoraire',
            name='altura',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='especificacionesprecalentadoraire',
            name='area_unidad',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='especificaciones_precalentador_aire_area_unidad', to='intercambiadores.unidades'),
        ),
        migrations.AlterField(
            model_name='especificacionesprecalentadoraire',
            name='diametro',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='especificacionesprecalentadoraire',
            name='espesor',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='especificacionesprecalentadoraire',
            name='longitud_unidad',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='especificaciones_precalentador_aire_longitud_unidad', to='intercambiadores.unidades'),
        ),
        migrations.AlterField(
            model_name='especificacionesprecalentadoraire',
            name='material',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
        migrations.AlterField(
            model_name='especificacionesprecalentadoraire',
            name='temp_unidad',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='especificaciones_precalentador_aire_temp_unidad', to='intercambiadores.unidades'),
        ),
        migrations.AlterField(
            model_name='especificacionesprecalentadoraire',
            name='u_unidad',
            field=models.ForeignKey(default=27, on_delete=django.db.models.deletion.CASCADE, related_name='especificaciones_precalentador_aire_u_unidad', to='intercambiadores.unidades'),
        ),
    ]
