# Generated by Django 4.1.3 on 2023-01-04 23:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('insects', '0012_bug_site_week'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bug_site',
            name='bug',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='insects.bug'),
        ),
    ]
