# Generated by Django 3.0.1 on 2020-05-17 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('the_elder_commands', '0018_rename_esl_to_is_esl'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Character',
            new_name='Skills',
        ),
    ]