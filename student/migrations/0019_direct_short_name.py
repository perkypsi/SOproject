# Generated by Django 4.0.7 on 2022-10-22 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0018_direct_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='direct',
            name='short_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Краткое название комитета'),
        ),
    ]