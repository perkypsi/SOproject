# Generated by Django 4.0.7 on 2022-09-06 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='patronymic',
            field=models.CharField(blank=True, max_length=100, verbose_name='Отчество пользователя'),
        ),
    ]
