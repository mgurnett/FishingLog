# Generated by Django 4.1.3 on 2023-01-11 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catches', '0059_lake_week_log_week'),
    ]

    operations = [
        migrations.AddField(
            model_name='temp',
            name='week',
            field=models.ManyToManyField(blank=True, to='catches.week'),
        ),
    ]