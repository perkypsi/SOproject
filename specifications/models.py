from django.db import models


class Document(models.Model):
    document = models.FileField(upload_to='documents/')
    name = models.CharField('Название документа', max_length=100, blank=True, null=True)
    description = models.TextField('Описание документа', max_length=10000, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
