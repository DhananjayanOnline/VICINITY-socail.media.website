# Generated by Django 4.0.3 on 2022-04-11 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0040_alter_post_creatorid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='postid',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
