# Generated by Django 4.1.3 on 2023-01-04 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insects', '0007_hatch'),
    ]

    operations = [
        migrations.AddField(
            model_name='hatch',
            name='weeks',
            field=models.ManyToManyField(to='insects.week'),
        ),
    ]
