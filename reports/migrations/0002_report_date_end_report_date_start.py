# Generated by Django 4.0.7 on 2022-10-28 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='date_end',
            field=models.DateField(blank=True, null=True, verbose_name='Дата окончания мероприятия'),
        ),
        migrations.AddField(
            model_name='report',
            name='date_start',
            field=models.DateField(blank=True, null=True, verbose_name='Дата начала мероприятия'),
        ),
    ]
