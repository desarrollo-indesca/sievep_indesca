# Generated by Django 4.2.4 on 2023-10-10 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intercambiadores', '0026_remove_unidades_valor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propiedadestubocarcasa',
            name='diametro_externo_tubos',
            field=models.DecimalField(decimal_places=4, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='propiedadestubocarcasa',
            name='diametro_interno_tubos',
            field=models.DecimalField(decimal_places=4, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='propiedadestubocarcasa',
            name='pitch_tubos',
            field=models.DecimalField(decimal_places=4, max_digits=8, null=True),
        ),
    ]
