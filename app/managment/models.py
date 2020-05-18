from django.utils import timezone
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from lk.models import Doctors


# таблица всех записай
class Record(models.Model):
    class Meta:
        verbose_name = 'запись'
        verbose_name_plural = 'Записи'

    STATUSES = (
        ('Открыт', 'Открыт'),
        ('Закрыт', 'Закрыт'),
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пациент',
        on_delete=models.CASCADE,
        default=None
    )
    doctor = models.ForeignKey(
        Doctors,
        verbose_name='Доктор',
        on_delete=models.CASCADE,
        default=None
    )
    time = models.DateTimeField("Дата/время", default=timezone.now, blank=True)
    status = models.CharField(
        "Статус записи",
        max_length=60,
        choices=STATUSES,
        default='Открыт'
    )
    diagnosis = models.TextField(
        "Диагноз", max_length=255, default='', blank=True)

    def __str__(self):
        return self.user.profile.fio


class Notworkday(models.Model):
    class Meta:
        verbose_name = 'нерабочий день'
        verbose_name_plural = 'Нерабочие дни'

    doctor = models.ForeignKey(
        Doctors,
        verbose_name='Доктор',
        on_delete=models.DO_NOTHING,
        default=None
    )

    not_work_day = models.DateField(
        'Нерабочие дни', blank=True, default=datetime.min.date())

    def __str__(self):
        return str(self.not_work_day)


class Contact(models.Model):
    class Meta:
        verbose_name = 'обратная связь'
        verbose_name_plural = 'Обратная связь'

    subject = models.CharField('Тема сообщения', max_length=100)
    sender = models.EmailField('Email')
    message = models.TextField('Сообщение', max_length=800)

    answer = models.TextField('Ответ', max_length=800, blank=False, default='')
    send = models.BooleanField('Ответ написан', default=False)
    answered = models.BooleanField('Ответ отправлен', default=False)

    def __str__(self):
        return self.subject
