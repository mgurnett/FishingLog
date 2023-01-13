# Generated by Django 4.1.3 on 2023-01-13 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catches', '0064_remove_hatch_strength'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lake',
            name='week',
        ),
        migrations.AlterField(
            model_name='lake',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catches.region'),
        ),
    ]
