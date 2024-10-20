# Generated by Django 4.2.4 on 2023-12-21 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intercambiadores', '0066_alter_intercambiador_efectividad_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluacionesintercambiador',
            name='ua',
        ),
        migrations.AlterField(
            model_name='evaluacionesintercambiador',
            name='cp_carcasa_gas',
            field=models.DecimalField(decimal_places=4, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='evaluacionesintercambiador',
            name='cp_carcasa_liquido',
            field=models.DecimalField(decimal_places=4, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='evaluacionesintercambiador',
            name='cp_tubo_gas',
            field=models.DecimalField(decimal_places=4, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='evaluacionesintercambiador',
            name='cp_tubo_liquido',
            field=models.DecimalField(decimal_places=4, max_digits=12, null=True),
        ),
    ]
