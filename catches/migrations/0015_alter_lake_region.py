# Generated by Django 4.1.3 on 2022-12-11 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catches', '0014_remove_fly_bug_fly_bug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lake',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catches.region'),
        ),
    ]