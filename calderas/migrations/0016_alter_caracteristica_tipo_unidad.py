# Generated by Django 4.2.4 on 2024-07-08 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('intercambiadores', '0072_alter_clasesunidades_table'),
        ('calderas', '0015_alter_composicioncombustible_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caracteristica',
            name='tipo_unidad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='intercambiadores.clasesunidades'),
        ),
    ]
