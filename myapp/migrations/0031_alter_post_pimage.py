# Generated by Django 4.0.3 on 2022-04-10 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0030_alter_post_creatorid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='pimage',
            field=models.ImageField(blank=True, default='x', upload_to='images/'),
        ),
    ]