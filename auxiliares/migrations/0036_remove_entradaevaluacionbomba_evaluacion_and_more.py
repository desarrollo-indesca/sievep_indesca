# Generated by Django 4.2.4 on 2024-04-09 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('intercambiadores', '0068_propiedadesdobletubo_altura_aletas_and_more'),
        ('auxiliares', '0035_remove_entradaevaluacionbomba_evaluacion_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entradaevaluacionbomba',
            name='evaluacion',
        ),
        migrations.RemoveField(
            model_name='salidaevaluacionbombageneral',
            name='evaluacion',
        ),
        migrations.AddField(
            model_name='salidaevaluacionbombageneral',
            name='fluido',
            field=models.ForeignKey(default=73, on_delete=django.db.models.deletion.PROTECT, related_name='fluido_salidaevaluacionbomba', to='intercambiadores.fluido'),
            preserve_default=False,
        ),
    ]
