# Generated by Django 4.0.7 on 2022-10-30 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('specifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='description',
            field=models.TextField(blank=True, max_length=10000, verbose_name='Описание документа'),
        ),
    ]
