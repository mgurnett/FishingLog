# Generated by Django 4.1.3 on 2023-01-11 21:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catches', '0055_week_chart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chart',
            name='hatch',
        ),
    ]