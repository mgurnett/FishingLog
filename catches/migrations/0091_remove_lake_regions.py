# Generated by Django 4.2.7 on 2024-03-28 21:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catches", "0090_lake_regions_region_lakes_delete_userregion"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="lake",
            name="regions",
        ),
    ]