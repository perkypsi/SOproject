# Generated by Django 4.0.7 on 2022-10-09 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0011_alter_profile_rating_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='external_documentation',
            field=models.BooleanField(default=False, verbose_name='Необходимость в помощи у ИН'),
        ),
        migrations.AddField(
            model_name='event',
            name='info_documentation',
            field=models.BooleanField(default=False, verbose_name='Необходимость в помощи у ИН'),
        ),
        migrations.AddField(
            model_name='event',
            name='project_documentation',
            field=models.BooleanField(default=False, verbose_name='Необходимость в помощи у ИН'),
        ),
    ]
