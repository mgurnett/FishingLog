# Generated by Django 4.2.7 on 2024-03-19 04:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="address",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.address",
            ),
        ),
    ]
