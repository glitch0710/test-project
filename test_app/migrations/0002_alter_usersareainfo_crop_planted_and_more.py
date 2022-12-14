# Generated by Django 4.1 on 2022-09-29 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersareainfo',
            name='crop_planted',
            field=models.CharField(blank=True, choices=[('Rice', 'Rice'), ('Corn', 'Corn'), ('Sugarcane', 'Sugarcane')], default='Rice', max_length=9, null=True),
        ),
        migrations.AlterField(
            model_name='usersareainfo',
            name='remarks',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
