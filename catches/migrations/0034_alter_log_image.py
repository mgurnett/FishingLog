# Generated by Django 4.1.3 on 2022-12-17 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catches', '0033_alter_log_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
