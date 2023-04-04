# Generated by Django 4.1.7 on 2023-04-03 04:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conferences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('nhl_id', models.IntegerField()),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Divisions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('nhl_id', models.IntegerField()),
                ('conferences', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nhl.conferences')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Teams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('nhl_id', models.IntegerField()),
                ('venue', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('teamName', models.CharField(max_length=100)),
                ('locationName', models.CharField(max_length=100)),
                ('divisions', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nhl.divisions')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
