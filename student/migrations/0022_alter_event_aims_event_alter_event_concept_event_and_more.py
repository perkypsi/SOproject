# Generated by Django 4.0.7 on 2022-10-28 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0021_profile_last_visit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='aims_event',
            field=models.TextField(blank=True, max_length=10000, verbose_name='Цели мероприятия'),
        ),
        migrations.AlterField(
            model_name='event',
            name='concept_event',
            field=models.TextField(blank=True, max_length=10000, verbose_name='Концепция мероприятия'),
        ),
        migrations.AlterField(
            model_name='event',
            name='document_for_external',
            field=models.CharField(blank=True, max_length=200, verbose_name='Ссылка на ТЗ для КВСК'),
        ),
        migrations.AlterField(
            model_name='event',
            name='document_for_info',
            field=models.CharField(blank=True, max_length=200, verbose_name='Ссылка на ТЗ для МН'),
        ),
        migrations.AlterField(
            model_name='event',
            name='external_documentation',
            field=models.BooleanField(default=False, verbose_name='ТЗ для КВСК одобрено'),
        ),
        migrations.AlterField(
            model_name='event',
            name='info_documentation',
            field=models.BooleanField(default=False, verbose_name='ТЗ для МН одобрено'),
        ),
        migrations.AlterField(
            model_name='event',
            name='need_external',
            field=models.BooleanField(default=False, verbose_name='Необходимость в помощи у КВСК'),
        ),
        migrations.AlterField(
            model_name='event',
            name='need_info',
            field=models.BooleanField(default=False, verbose_name='Необходимость в помощи у МК'),
        ),
    ]
