# Generated by Django 4.1.3 on 2022-12-09 04:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catches', '0003_remove_child_parent_delete_character_delete_child_and_more'),
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
                ('name', models.CharField(max_length=100, verbose_name='Name of fly')),
                ('fly_type', models.CharField(choices=[('dry', 'Dry fly'), ('nymph', 'Nymphs'), ('wet', 'Wet flys'), ('chronomid', 'Chronomids'), ('streamer', 'Streamers'), ('attractor', 'Attractor patterns'), ('other', 'Anything else')], max_length=100, verbose_name='Fly catagory')),
                ('description', models.CharField(blank=True, max_length=400, verbose_name='Description')),
                ('size_range', models.CharField(blank=True, max_length=100, verbose_name='Hook sizes')),
                ('author', models.CharField(blank=True, max_length=100, verbose_name='Author')),
                ('youtube', models.URLField(blank=True, verbose_name='YouTube video')),
                ('image', models.ImageField(blank=True, default='default.jpg', upload_to='', verbose_name='Picture of fly')),
                ('bug', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catches.bug')),
            ],
            options={
                'ordering': ['name'],
            },
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
                ('region', models.CharField(blank=True, max_length=100)),
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
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('catch_date', models.DateField(default=django.utils.timezone.now)),
                ('record_date', models.DateField(default=django.utils.timezone.now)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('watertemp', models.IntegerField(choices=[(1, '0 to 5 up'), (2, '6 up'), (3, '7 up'), (4, '8 up'), (5, '9 up'), (6, '10 up'), (7, '11 up'), (8, '12 up'), (9, '13 up'), (10, '14 up'), (11, '15 up'), (12, '16 up'), (13, '17 up'), (14, '18 up'), (15, '19 up'), (16, '20 up'), (17, '21 up'), (18, '22 up'), (19, 'above 22'), (20, '22 down'), (21, '21 down'), (22, '20 down'), (23, '19 down'), (24, '18 down'), (25, '17 down'), (26, '16 down'), (27, '15 down'), (28, '14 down'), (29, '13 down'), (30, '12 down'), (31, '11 down'), (32, '10 down'), (33, '9 down'), (34, '8 down'), (35, '7 down'), (36, '6 down'), (37, '5 down'), (38, '4 down to 0'), (100, None)], default=100)),
                ('length', models.FloatField(blank=True, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('fly_size', models.CharField(blank=True, max_length=100)),
                ('fly_colour', models.CharField(blank=True, max_length=100)),
                ('notes', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, default=None, upload_to='', verbose_name='Picture of fly')),
                ('fish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catches.fish')),
                ('fly', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catches.fly')),
                ('lake', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catches.lake')),
            ],
            options={
                'ordering': ['watertemp'],
            },
        ),
        migrations.AddField(
            model_name='lake',
            name='fish',
            field=models.ManyToManyField(blank=True, through='catches.Stock', to='catches.fish'),
        ),
    ]
