# Generated by Django 4.2.4 on 2023-10-30 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intercambiadores', '0034_rename_fluido_cp_condicionestubocarcasa_fluido_cp_gas_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='condicionestubocarcasa',
            name='tipo_cp',
            field=models.CharField(choices=[['M', 'Manual'], ['A', 'Automático']], default='A', max_length=1),
            preserve_default=False,
        ),
    ]
