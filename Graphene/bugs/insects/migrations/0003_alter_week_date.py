# Generated by Django 4.1.3 on 2023-01-04 17:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('insects', '0002_alter_week_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='week',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
