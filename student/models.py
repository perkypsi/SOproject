from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models


class StatusEvent(models.Model):
    name = models.CharField("Статус мероприятия", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус мероприятия'
        verbose_name_plural = 'Статусы мероприятий'


class Direct(models.Model):
    name = models.CharField("Название комитета", max_length=50)
    short_name = models.CharField("Краткое название комитета", max_length=50, blank=True, null=True)
    id_name = models.CharField("Id комитета", max_length=50, blank=True, null=True)
    color = models.CharField("Цвет комитета", max_length=6, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Комитет'
        verbose_name_plural = 'Комитеты'


class AccessLevel(models.Model):
    name = models.CharField("Уровень доступа", max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Уровень доступа'
        verbose_name_plural = 'Уровни доступа'


class Profile(AbstractUser):
    patronymic = models.CharField("Отчество пользователя", max_length=100, blank=True)
    birthdate = models.DateField("Дата рождения пользователя", null=True, blank=True)
    direct = models.ForeignKey(Direct, verbose_name="Комитет", on_delete=models.PROTECT, null=True, blank=True)
    edu_group = models.CharField('Учебная группа', max_length=50, blank=True)
    phone_number = models.CharField("Номер телефона", max_length=20, blank=True)
    link_social = models.CharField("Ссылка на социальные сети", max_length=100, blank=True)
    access_level = models.ForeignKey(AccessLevel, verbose_name="Уровень доступа", on_delete=models.PROTECT, null=True,
                                     blank=True)
    rating = models.IntegerField("Рейтинг пользователя", null=True, blank=True)
    rating_score = models.IntegerField("Рейтинговые очки пользователя", null=True, blank=True)
    last_visit = models.DateField("Дата последнего посещения", null=True, blank=True)
    post = models.CharField("Должность пользователя", max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Notification(models.Model):
    title = models.CharField("Заголовок", max_length=50)
    content = models.TextField("Содержание", max_length=1000)
    profile = models.ForeignKey(Profile, verbose_name="Пользователь", on_delete=models.CASCADE, null=True,
                                blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'


class Event(models.Model):
    name_event = models.CharField('Название мероприятия', max_length=100)
    date_event = models.DateField('Дата проведения мероприятия', null=True, blank=True)
    direct_event = models.ForeignKey(Direct, verbose_name="Комитет мероприятия", on_delete=models.PROTECT)
    name_author = models.CharField('ФИО главного организатора', max_length=100, blank=True)
    email_author = models.CharField('email главного организатора', max_length=100, blank=True)
    phone_author = models.CharField('Телефонный номер главного организатора', max_length=20, blank=True)
    aims_event = models.TextField('Цели мероприятия', max_length=10000, blank=True)
    concept_event = models.TextField('Концепция мероприятия', max_length=10000, blank=True)
    amount_participants = models.IntegerField('Количество участников', default=0, blank=True)
    place_event = models.TextField('Место проведения мероприятия', max_length=1000, blank=True)
    status = models.ForeignKey(StatusEvent, verbose_name="Статус мероприятия", on_delete=models.PROTECT, null=True, blank=True)

    main_organizer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='main_event', null=True, blank=True)
    part_list = models.ManyToManyField(Profile, related_name='part_list', blank=True)
    queue_list = models.ManyToManyField(Profile, related_name='queue_list', blank=True)

    need_info = models.BooleanField('Необходимость в помощи у МК', default=False)
    need_external = models.BooleanField('Необходимость в помощи у КВСК', default=False)

    document_for_info = models.CharField('Ссылка на ТЗ для МН', max_length=200, blank=True)
    info_uploaded_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    document_for_external = models.CharField('Ссылка на ТЗ для КВСК', max_length=200, blank=True)
    external_uploaded_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    additional_document = models.CharField('Ссылка на дополнительные документы', max_length=200, blank=True)
    additional_uploaded_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    step_one = models.TextField('Подготовка проекта', max_length=10000, blank=True)
    step_two = models.TextField('Реклама', max_length=10000, blank=True)
    step_three = models.TextField('Дистанционный этап', max_length=10000, blank=True)
    step_four = models.TextField('Очный этап', max_length=10000, blank=True)
    step_five = models.TextField('Подведение итогов', max_length=10000, blank=True)

    project_documentation = models.BooleanField('Папка проекта одобрена', default=False)
    info_documentation = models.BooleanField('ТЗ для МН одобрено', default=False)
    external_documentation = models.BooleanField('ТЗ для КВСК одобрено', default=False)

    mendeleev_bonus = models.BooleanField('Добавлено ли в менделеев бонус', default=False)

    def __str__(self):
        return self.name_event

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'


class Ban(models.Model):
    profile = models.OneToOneField(Profile, verbose_name="Профиль", on_delete=models.CASCADE)
    datetime = models.DateTimeField(verbose_name='Период блокировки', null=True, blank=True)

    def __str__(self):
        return self.profile.username

    class Meta:
        verbose_name = 'Блокировка'
        verbose_name_plural = 'Блокировки'



