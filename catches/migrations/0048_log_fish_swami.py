# Generated by Django 4.1.3 on 2022-12-29 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catches', '0047_alter_fly_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='fish_swami',
            field=models.IntegerField(blank=True, default=0),
            preserve_default=False,
        ),
    ]