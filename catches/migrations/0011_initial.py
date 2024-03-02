# Generated by Django 4.1.3 on 2022-12-09 18:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catches', '0010_remove_bug_site_bug_remove_bug_site_lake_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Insect name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Fish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('notes', models.TextField(blank=True)),
                ('abbreviation', models.CharField(blank=True, max_length=10)),
                ('image', models.ImageField(blank=True, default='default.jpg', upload_to='')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Fly',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=400, verbose_name='Description')),
                ('size_range', models.CharField(blank=True, max_length=100, verbose_name='Hook sizes')),
                ('author', models.CharField(blank=True, max_length=100, verbose_name='Author')),
                ('youtube', models.URLField(blank=True, verbose_name='YouTube video')),
                ('image', models.ImageField(blank=True, default='default.jpg', upload_to='', verbose_name='Picture of fly')),
                ('bug', models.ManyToManyField(blank=True, to='catches.bug')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Fly_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('notes', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('notes', models.TextField(blank=True)),
                ('other_name', models.CharField(blank=True, max_length=100)),
                ('ats', models.CharField(blank=True, max_length=100)),
                ('lat', models.DecimalField(blank=True, decimal_places=10, max_digits=15, null=True)),
                ('long', models.DecimalField(blank=True, decimal_places=10, max_digits=15, null=True)),
                ('district', models.CharField(blank=True, max_length=100)),
                ('waterbody_id', models.IntegerField(blank=True, null=True)),
                ('favourite', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-favourite', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Temp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('notes', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date_stocked', models.DateField()),
                ('number', models.IntegerField()),
                ('length', models.FloatField()),
                ('strain', models.CharField(blank=True, choices=[('BEBE', 'Beitty x Beitty'), ('BRBE', 'Bow River x Beitty'), ('CLCL', 'Campbell Lake'), ('LYLY', 'Lyndon'), ('PLPL', 'Pit Lake'), ('TLTLJ', 'Trout Lodge / Jumpers'), ('TLTLK', 'Trout Lodge / Kamloops'), ('TLTLS', 'Trout Lodge / Silvers'), ('LSE', 'Lac Ste. Anne'), ('JBL', 'Job Lake')], max_length=100)),
                ('gentotype', models.CharField(blank=True, choices=[('2N', 'diploid'), ('3N', 'triploid'), ('AF2N', 'all-female diploid'), ('AF3N', 'all-female triploid')], max_length=100)),
                ('fish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catches.fish')),
                ('lake', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catches.lake')),
            ],
            options={
                'ordering': ['-date_stocked'],
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('catch_date', models.DateField(default=django.utils.timezone.now)),
                ('record_date', models.DateField(default=django.utils.timezone.now)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('length', models.FloatField(blank=True, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('fly_size', models.CharField(blank=True, max_length=100)),
                ('fly_colour', models.CharField(blank=True, max_length=100)),
                ('notes', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, default=None, upload_to='', verbose_name='Picture of fly')),
                ('fish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catches.fish')),
                ('fly', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catches.fly')),
                ('lake', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catches.lake')),
                ('temp', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='catches.temp')),
            ],
            options={
                'ordering': ['temp'],
            },
        ),
        migrations.AddField(
            model_name='lake',
            name='fish',
            field=models.ManyToManyField(blank=True, through='catches.Stock', to='catches.fish'),
        ),
        migrations.AddField(
            model_name='lake',
            name='region',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='catches.region'),
        ),
        migrations.AddField(
            model_name='fly',
            name='fly_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catches.fly_type'),
        ),
        migrations.CreateModel(
            name='Bug_site',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('notes', models.TextField(blank=True)),
                ('bug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catches.bug')),
                ('lake', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catches.lake')),
                ('temp', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='catches.temp')),
            ],
            options={
                'ordering': ['temp'],
            },
        ),
    ]
