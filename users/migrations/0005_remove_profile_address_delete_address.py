# Generated by Django 4.2.7 on 2024-03-19 04:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_profile_address"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="address",
        ),
        migrations.DeleteModel(
            name="Address",
        ),
    ]