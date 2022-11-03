# Generated by Django 4.0.7 on 2022-10-22 20:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0019_direct_short_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='main_organizer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='main_event', to=settings.AUTH_USER_MODEL),
        ),
    ]
