import datetime
from django.contrib.auth.models import User
from django.db import models


class Speciality(models.Model):
    class Meta:
        verbose_name = 'специальность'
        verbose_name_plural = 'Специальности врачей'

    speciality = models.CharField("Специальность", max_length=100)

    def __str__(self):
        return self.speciality


class Doctors(models.Model):
    class Meta:
        verbose_name = 'врача'
        verbose_name_plural = 'Врачи'
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, default=None)
    name = models.CharField("ФИО", max_length=100, default='')
    DAYS_OF_THE_WEEK = (
        ('ПН', 'Понедельник'),
        ('ВТ', 'Вторник'),
        ('СР', 'Среда'),
        ('ЧТ', 'Четверг'),
        ('ПТ', 'Пятнца'),
        ('СБ', 'Суббота'),
        ('ВС', 'Воскресенье'),
    )
    specialty = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    start_day_work = models.CharField(
        "Начало работы",
        max_length=60,
        choices=DAYS_OF_THE_WEEK,
        default='ПН'
    )
    end_day_work = models.CharField(
        "Конец работы",
        max_length=60,
        choices=DAYS_OF_THE_WEEK,
        default='ПТ'
    )
    room = models.IntegerField("Кабинет", default=0)
    avatar = models.ImageField(
        "Аватар",
        blank=True,
        upload_to='doc_avatar',
        default="default_doc.png"
    )

    def get_full_doc_str(self):
        return self.specialty + " " + self.name

    def __str__(self):
        return self.name


class Schedule(models.Model):
    class Meta:
        verbose_name = 'расписание'
        verbose_name_plural = 'Расписание врача'

    doctor = models.OneToOneField(
        Doctors,
        verbose_name='Доктор',
        on_delete=models.DO_NOTHING
    )

    mo_start = models.TimeField("Понедельник начало", blank=True)
    mo_end = models.TimeField("Понедельник конец", blank=True)

    tu_start = models.TimeField("Вторник начало", blank=True)
    tu_end = models.TimeField("Вторник конец", blank=True)

    we_start = models.TimeField("Среда начало", blank=True)
    we_end = models.TimeField("Среда конец", blank=True)

    th_start = models.TimeField("Четверг начало", blank=True)
    th_end = models.TimeField("Четверг конец", blank=True)

    fr_start = models.TimeField("Пятница начало", blank=True)
    fr_end = models.TimeField("Пятница конец", blank=True)

    time_step = models.TimeField(
        "Время на одного пациента",
        blank=True,
        default=datetime.time(00, 00)
    )

    def __str__(self):
        return self.doctor.name
