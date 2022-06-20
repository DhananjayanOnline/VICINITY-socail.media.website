# Generated by Django 4.0.3 on 2022-05-02 04:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0050_alter_announcement_created_alter_announcement_expiry'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='panchayath',
            field=models.CharField(default='x', max_length=40),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='created',
            field=models.DateField(default=datetime.datetime(2022, 5, 2, 9, 32, 58, 208786)),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='expiry',
            field=models.DateField(default=datetime.datetime(2022, 5, 4, 9, 32, 58, 208786)),
        ),
    ]