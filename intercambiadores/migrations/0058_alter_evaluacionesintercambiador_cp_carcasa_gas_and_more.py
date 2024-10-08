# Generated by Django 4.2.4 on 2023-11-28 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intercambiadores', '0057_rename_diametro_interno_tubos_propiedadestubocarcasa_diametro_interno_carcasa_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluacionesintercambiador',
            name='cp_carcasa_gas',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='evaluacionesintercambiador',
            name='cp_carcasa_liquido',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='evaluacionesintercambiador',
            name='cp_tubo_gas',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='evaluacionesintercambiador',
            name='cp_tubo_liquido',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='evaluacionesintercambiador',
            name='temp_ex_entrada',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
        migrations.AlterField(
            model_name='evaluacionesintercambiador',
            name='temp_ex_salida',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
        migrations.AlterField(
            model_name='evaluacionesintercambiador',
            name='temp_in_entrada',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
        migrations.AlterField(
            model_name='evaluacionesintercambiador',
            name='temp_in_salida',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]
