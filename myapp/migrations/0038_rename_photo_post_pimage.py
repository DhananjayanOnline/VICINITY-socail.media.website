# Generated by Django 4.0.3 on 2022-04-11 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0037_alter_post_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='photo',
            new_name='pimage',
        ),
    ]
