# Generated by Django 4.2.4 on 2023-09-20 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intercambiadores', '0008_condicionestubocarcasa_flujo_liquido_entrada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condicionestubocarcasa',
            name='fouling',
            field=models.DecimalField(decimal_places=9, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='condicionestubocarcasa',
            name='temp_entrada',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
        migrations.AlterField(
            model_name='condicionestubocarcasa',
            name='temp_salida',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]
