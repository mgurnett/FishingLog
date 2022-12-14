# Generated by Django 4.1.3 on 2022-12-09 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catches', '0008_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bug_site',
            name='temp',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='catches.temp'),
        ),
        migrations.AlterField(
            model_name='fly',
            name='fly_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catches.fly_type'),
        ),
        migrations.AlterField(
            model_name='lake',
            name='region',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='catches.region'),
        ),
        migrations.AlterField(
            model_name='log',
            name='fly',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='catches.fly'),
        ),
        migrations.AlterField(
            model_name='log',
            name='temp',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='catches.temp'),
        ),
    ]
