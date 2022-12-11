# Generated by Django 4.1.3 on 2022-12-09 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catches', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('movie', models.ManyToManyField(to='catches.movie')),
            ],
        ),
    ]