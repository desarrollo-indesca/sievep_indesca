# Generated by Django 4.2.4 on 2023-10-06 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intercambiadores', '0024_alter_evaluacionesintercambiador_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluacionesintercambiador',
            name='ensuciamiento',
            field=models.DecimalField(decimal_places=5, max_digits=15),
        ),
    ]
