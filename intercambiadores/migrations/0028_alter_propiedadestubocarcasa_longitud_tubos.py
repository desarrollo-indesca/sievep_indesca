# Generated by Django 4.2.4 on 2023-10-10 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intercambiadores', '0027_alter_propiedadestubocarcasa_diametro_externo_tubos_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propiedadestubocarcasa',
            name='longitud_tubos',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
    ]
