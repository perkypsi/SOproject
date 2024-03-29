# Generated by Django 4.0.7 on 2022-10-31 20:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.IntegerField(max_length=100, verbose_name='Id чата с пользователем в Telegram')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bot', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Бот',
                'verbose_name_plural': 'Боты',
            },
        ),
    ]
