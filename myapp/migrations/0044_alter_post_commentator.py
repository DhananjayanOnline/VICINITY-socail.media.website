# Generated by Django 4.0.3 on 2022-04-30 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0043_post_commentator_alter_post_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='commentator',
            field=models.CharField(max_length=30),
        ),
    ]