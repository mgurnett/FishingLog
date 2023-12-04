# Generated by Django 5.0 on 2023-12-04 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catches", "0074_alter_fly_type_notes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stock",
            name="strain",
            field=models.CharField(
                blank=True,
                choices=[
                    ("BEBE", "Beitty x Beitty"),
                    ("BRBE", "Bow River x Beitty"),
                    ("CLCL", "Campbell Lake"),
                    ("LYLY", "Lyndon"),
                    ("PLPL", "Pit Lake"),
                    ("TLTLJ", "Trout Lodge / Jumpers"),
                    ("TLTLK", "Trout Lodge / Kamloops"),
                    ("TLTLS", "Trout Lodge / Silvers"),
                    ("LSE", "Lac Ste. Anne"),
                    ("JBL", "Job Lake"),
                    ("MC", "Marie Creek"),
                    ("RI", "Rock Island"),
                    ("AC", "Allison Creek"),
                    ("RD", "Riverance"),
                ],
                max_length=100,
            ),
        ),
    ]
