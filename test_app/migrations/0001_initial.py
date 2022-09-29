# Generated by Django 4.1 on 2022-09-29 06:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaCrop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crop_planted', models.CharField(choices=[('Rice', 'Rice'), ('Corn', 'Corn'), ('Sugarcane', 'Sugarcane')], default='Rice', max_length=9)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('remarks', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BrgyCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brgy_psgc_code', models.CharField(max_length=20)),
                ('brgy_name', models.CharField(max_length=200)),
                ('region_code', models.IntegerField()),
                ('province_code', models.IntegerField()),
                ('muncity_code', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Farmer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_id', models.CharField(blank=True, max_length=20, null=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('middle_name', models.CharField(max_length=200)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=1)),
                ('region', models.CharField(max_length=200)),
                ('province', models.CharField(max_length=200)),
                ('muncity', models.CharField(max_length=200)),
                ('brgy', models.CharField(max_length=200)),
                ('address', models.TextField(blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('contact_no', models.CharField(blank=True, max_length=20, null=True)),
                ('tin', models.CharField(blank=True, max_length=20, null=True)),
                ('philhealth', models.CharField(blank=True, max_length=20, null=True)),
                ('sss', models.CharField(blank=True, max_length=20, null=True)),
                ('pagibig', models.CharField(blank=True, max_length=20, null=True)),
                ('civil_status', models.CharField(blank=True, max_length=20, null=True)),
                ('nationality', models.CharField(blank=True, max_length=50, null=True)),
                ('birthdate', models.DateField(default=None)),
                ('spouse', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MunCityCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('muncity_psgc_code', models.CharField(max_length=20)),
                ('muncity_name', models.CharField(max_length=200)),
                ('region_code', models.IntegerField()),
                ('province_code', models.IntegerField()),
                ('muncity_code', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ProvincialCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prov_psgc_code', models.CharField(max_length=20)),
                ('province_name', models.CharField(max_length=200)),
                ('region_code', models.IntegerField()),
                ('prov_code', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RegionCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('psgc_code', models.CharField(max_length=20)),
                ('region_name', models.CharField(max_length=200)),
                ('reg_code', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UsersAreaInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_area', models.FloatField()),
                ('crop_planted', models.CharField(choices=[('Rice', 'Rice'), ('Corn', 'Corn'), ('Sugarcane', 'Sugarcane')], default='Rice', max_length=9)),
                ('remarks', models.CharField(max_length=100)),
                ('sketch_plan', models.FileField(blank=True, max_length=254, upload_to='documents_sp/')),
                ('map', models.FileField(blank=True, max_length=254, upload_to='documents_map/')),
                ('google_earth', models.FileField(blank=True, max_length=254, upload_to='documents_ge/')),
                ('area_coordinates', models.FileField(blank=True, max_length=254, upload_to='documents_coordinates/')),
                ('profile_field', models.CharField(max_length=250)),
                ('soil_ph', models.IntegerField()),
                ('region', models.CharField(max_length=200)),
                ('province', models.CharField(max_length=200)),
                ('muncity', models.CharField(max_length=200)),
                ('brgy', models.CharField(max_length=200)),
                ('farmer_id', models.ForeignKey(db_column='farmer_id', on_delete=django.db.models.deletion.CASCADE, to='test_app.farmer')),
            ],
        ),
        migrations.CreateModel(
            name='ProfileAttachments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_picture', models.FileField(upload_to='profile_attachments/id/%Y%m%d')),
                ('cedula', models.FileField(upload_to='profile_attachments/cedula/%Y%m%d')),
                ('brgy_clearance', models.FileField(upload_to='profile_attachments/brgy_clearance/%Y%m%d')),
                ('tax_dec', models.FileField(upload_to='profile_attachments/tax_dec/%Y%m%d')),
                ('valid_id_one', models.FileField(upload_to='profile_attachments/valid_id/%Y%m%d')),
                ('valid_id_two', models.FileField(upload_to='profile_attachments/valid_id/%Y%m%d')),
                ('farmer_id', models.ForeignKey(db_column='farmer_id', on_delete=django.db.models.deletion.CASCADE, to='test_app.farmer')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=1)),
                ('region', models.CharField(max_length=200)),
                ('province', models.CharField(max_length=200)),
                ('muncity', models.CharField(max_length=200)),
                ('brgy', models.CharField(max_length=200)),
                ('address', models.TextField()),
                ('income_annual', models.FloatField(blank=True, default=0, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FarmerDependents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dependent_name', models.CharField(max_length=250)),
                ('age', models.IntegerField()),
                ('farmer', models.ForeignKey(db_column='farmer', on_delete=django.db.models.deletion.CASCADE, to='test_app.farmer')),
            ],
        ),
    ]
