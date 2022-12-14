# Generated by Django 4.1.3 on 2022-12-11 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catches', '0012_remove_log_name_remove_stock_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fly',
            name='author',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='fly',
            name='description',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='fly',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', upload_to=''),
        ),
        migrations.AlterField(
            model_name='fly',
            name='size_range',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='fly',
            name='youtube',
            field=models.URLField(blank=True),
        ),
    ]
