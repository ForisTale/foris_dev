# Generated by Django 3.0.1 on 2020-04-15 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('the_elder_commands', '0011_unique_variants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plugins',
            name='plugin_name',
            field=models.TextField(default='', unique=True),
        ),
    ]