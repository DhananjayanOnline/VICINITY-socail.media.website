# Generated by Django 4.0.3 on 2022-04-11 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0039_alter_post_pimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='creatorid',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
