# Generated by Django 4.0.7 on 2022-10-30 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0025_profile_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='link_telegram',
        ),
    ]
