# Generated by Django 4.2 on 2024-10-03 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catches', '0101_alter_article_notes_alter_bug_notes_alter_fish_notes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lake',
            name='reg_location',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]