# Generated by Django 4.0.3 on 2022-04-05 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_message_uname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='uname',
            field=models.CharField(max_length=30),
        ),
    ]
