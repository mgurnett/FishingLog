# Generated by Django 4.1.3 on 2022-12-15 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catches', '0021_tag_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='author',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
