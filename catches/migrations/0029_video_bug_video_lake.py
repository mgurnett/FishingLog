# Generated by Django 4.1.3 on 2022-12-16 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catches', '0028_remove_bug_youtube_remove_fish_youtube_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='bug',
            field=models.ManyToManyField(blank=True, to='catches.bug'),
        ),
        migrations.AddField(
            model_name='video',
            name='lake',
            field=models.ManyToManyField(blank=True, to='catches.lake'),
        ),
    ]
