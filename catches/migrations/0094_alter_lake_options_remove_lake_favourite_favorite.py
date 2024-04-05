# Generated by Django 4.2.7 on 2024-04-05 03:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("catches", "0093_alter_region_name"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="lake",
            options={"ordering": ["name"]},
        ),
        migrations.RemoveField(
            model_name="lake",
            name="favourite",
        ),
        migrations.CreateModel(
            name="Favorite",
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
                ("date_added", models.DateField(auto_now_add=True)),
                ("new_flag", models.DateField(auto_now_add=True)),
                (
                    "lake",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="catches.lake"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
