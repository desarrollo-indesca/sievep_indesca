# Generated by Django 4.2.4 on 2023-12-14 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('intercambiadores', '0064_intercambiador_ntu'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='intercambiador',
            name='ensuciamiento',
        ),
    ]
