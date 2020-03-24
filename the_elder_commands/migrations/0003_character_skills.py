# Generated by Django 2.2.3 on 2019-08-13 13:06

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('the_elder_commands', '0002_character_session_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='skills',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]