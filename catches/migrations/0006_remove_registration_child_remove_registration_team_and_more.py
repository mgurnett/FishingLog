# Generated by Django 4.1.3 on 2022-12-09 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catches', '0005_child_registration_team_registration_team'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registration',
            name='child',
        ),
        migrations.RemoveField(
            model_name='registration',
            name='team',
        ),
        migrations.RemoveField(
            model_name='team',
            name='children',
        ),
        migrations.DeleteModel(
            name='Child',
        ),
        migrations.DeleteModel(
            name='Registration',
        ),
        migrations.DeleteModel(
            name='Team',
        ),
    ]