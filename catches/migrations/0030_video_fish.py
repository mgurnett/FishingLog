# Generated by Django 4.1.3 on 2022-12-16 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catches', '0029_video_bug_video_lake'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='fish',
            field=models.ManyToManyField(blank=True, to='catches.fish'),
        ),
    ]