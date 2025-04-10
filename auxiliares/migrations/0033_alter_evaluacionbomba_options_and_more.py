# Generated by Django 4.2.4 on 2024-04-08 08:36

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auxiliares', '0032_remove_entradatramos_lado_entradatramos_salida_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='evaluacionbomba',
            options={'ordering': ('-fecha',)},
        ),
        migrations.RenameField(
            model_name='evaluacionbomba',
            old_name='usuario',
            new_name='creado_por',
        ),
        migrations.AlterField(
            model_name='entradaevaluacionbomba',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='entradatramos',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='evaluacionbomba',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='salidaevaluacionbombageneral',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='salidaseccionesevaluacionbomba',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='tuberiainstalacionbomba',
            name='diametro_tuberia',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Diámetro Interno'),
        ),
        migrations.AlterField(
            model_name='tuberiainstalacionbomba',
            name='longitud_tuberia',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Longitud Total'),
        ),
    ]
