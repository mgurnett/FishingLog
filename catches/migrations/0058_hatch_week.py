# Generated by Django 4.1.3 on 2023-01-11 21:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catches', '0057_chart_bug'),
    ]

    operations = [
        migrations.AddField(
            model_name='hatch',
            name='week',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catches.week'),
        ),
    ]