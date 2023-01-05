# Generated by Django 4.1.3 on 2023-01-05 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insects', '0018_temp_week_numbers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hatch',
            name='date',
        ),
        migrations.AddField(
            model_name='hatch',
            name='strength',
            field=models.IntegerField(choices=[('none', 0), ('few', 1), ('weak', 2), ('low', 3), ('lots', 4), ('abundent', 5)], default=0, max_length=100),
        ),
    ]
