# Generated by Django 4.1.3 on 2022-12-17 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catches', '0031_bug_site_tag_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='image',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Picture of catch'),
        ),
    ]
