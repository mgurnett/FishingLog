# Generated by Django 4.1.3 on 2023-01-15 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catches', '0065_remove_lake_week_alter_lake_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='hatch',
            name='temp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catches.temp'),
        ),
    ]