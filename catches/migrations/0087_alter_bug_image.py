# Generated by Django 4.2.7 on 2024-03-24 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catches", "0086_remove_bug_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bug",
            name="image",
            field=models.ImageField(
                default=None, upload_to="bug/", verbose_name="Picture of the bug"
            ),
        ),
    ]
