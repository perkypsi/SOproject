# Generated by Django 4.0.7 on 2022-10-28 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0022_alter_event_aims_event_alter_event_concept_event_and_more'),
        ('reports', '0002_report_date_end_report_date_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='event',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.event', verbose_name='Мероприятие'),
        ),
    ]
