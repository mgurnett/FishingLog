# Generated by Django 4.1.3 on 2023-01-16 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catches', '0068_hatch_catch_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hatch',
            old_name='catch_date',
            new_name='sight_date',
        ),
    ]
