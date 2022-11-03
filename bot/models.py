from django.db import models


from student.models import Profile


class Bot(models.Model):
    profile = models.OneToOneField(Profile, related_name='bot', on_delete=models.CASCADE)
    chat_id = models.IntegerField('Id чата с пользователем в Telegram', null=True, blank=True)

    def __str__(self):
        return self.profile.username

    class Meta:
        verbose_name = 'Бот'
        verbose_name_plural = 'Боты'
