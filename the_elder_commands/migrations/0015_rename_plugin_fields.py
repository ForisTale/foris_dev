# Generated by Django 3.0.1 on 2020-04-16 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('the_elder_commands', '0014_rename_variants_fields'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plugins',
            old_name='plugin_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='plugins',
            old_name='plugin_usable_name',
            new_name='usable_name',
        ),
    ]
