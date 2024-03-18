# Generated by Django 4.2.7 on 2024-03-18 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("address", models.CharField(blank=True, max_length=100)),
                ("city", models.CharField(blank=True, max_length=15)),
                ("prov", models.CharField(blank=True, max_length=5)),
            ],
        ),
    ]
