# Generated by Django 4.2.4 on 2024-04-22 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auxiliares', '0046_rename_condiciones_diseno_ventilador_condiciones_generales_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ventilador',
            name='condiciones_generales',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auxiliares.condicionesgeneralesventilador'),
        ),
    ]
