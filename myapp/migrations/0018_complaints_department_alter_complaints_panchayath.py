# Generated by Django 4.0.3 on 2022-04-05 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_complaints_panchayath'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaints',
            name='department',
            field=models.CharField(default='x', max_length=100),
        ),
        migrations.AlterField(
            model_name='complaints',
            name='panchayath',
            field=models.CharField(max_length=100),
        ),
    ]