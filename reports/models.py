from django.db import models

from student.models import Event, Profile



class Report(models.Model):
    event = models.OneToOneField(Event, verbose_name="Мероприятие", on_delete=models.CASCADE, null=True, blank=True)
    date_start = models.DateField('Дата начала мероприятия', null=True, blank=True)
    date_end = models.DateField('Дата окончания мероприятия', null=True, blank=True)
    real_amount_participants = models.IntegerField('Реальный охват (кол-во человек)', default=0, blank=True)
    problems = models.TextField('Реальные проблемы, возникшие при проведении мероприятия или его организации, и их решения', max_length=10000, blank=True)
    need_info = models.BooleanField('Потребовалась ли помощь медиа комитета при организации мероприятия?', default=False)
    need_external = models.BooleanField('Потребовалась ли помощь комитета внешних связей и коммуникации при организации мероприятия?', default=False)


    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'


class EvaluateOrganizer(models.Model):
    report = models.ForeignKey(Report, related_name="report", verbose_name="Отчет по мероприятию", on_delete=models.CASCADE, null=True, blank=True)
    profile = models.ForeignKey(Profile, related_name="profile", verbose_name="Пользователь", on_delete=models.CASCADE)
    evaluate = models.IntegerField('Оценка организатора в мероприятии', default=1)

    def __str__(self):
        return f"{self.report.event.name_event} --> {self.profile.username}"

    class Meta:
        verbose_name = 'Оценка организатора'
        verbose_name_plural = 'Оценки организаторов'


class Scholarship(models.Model):
    profile = models.OneToOneField(Profile, verbose_name="Пользователь", on_delete=models.CASCADE)
    evaluate = models.IntegerField('Оценка ПГАС председателем', default=0)

    def __str__(self):
        return self.profile.username

    class Meta:
        verbose_name = 'Оценка ПГАС'
        verbose_name_plural = 'Оценки ПГАС'