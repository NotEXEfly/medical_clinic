from django.contrib.auth.models import User
from django.db import models

# расширение таблицы User
class Profile(models.Model):
    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'Профиль пользователя'

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    fio = models.CharField("ФИО", max_length=100, default='')
    avatar = models.ImageField(
        "Аватар", blank=True, upload_to='user_avatar', default="default.png")

    def get_only_firstname(self):
        return self.fio.split(' ')[1]

    def get_only_surname(self):
        return self.fio.split(' ')[0]

    def get_only_patronymic(self):
        return self.fio.split(' ')[2]

    def __str__(self):
        return self.fio
