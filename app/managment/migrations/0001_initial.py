# Generated by Django 3.0.6 on 2020-05-18 03:29

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lk', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100, verbose_name='Тема сообщения')),
                ('sender', models.EmailField(max_length=254, verbose_name='Email')),
                ('message', models.TextField(max_length=800, verbose_name='Сообщение')),
                ('answer', models.TextField(default='', max_length=800, verbose_name='Ответ')),
                ('send', models.BooleanField(default=False, verbose_name='Ответ написан')),
                ('answered', models.BooleanField(default=False, verbose_name='Ответ отправлен')),
            ],
            options={
                'verbose_name': 'обратная связь',
                'verbose_name_plural': 'Обратная связь',
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Дата/время')),
                ('status', models.CharField(choices=[('Открыт', 'Открыт'), ('Закрыт', 'Закрыт')], default='Открыт', max_length=60, verbose_name='Статус записи')),
                ('diagnosis', models.TextField(blank=True, default='', max_length=255, verbose_name='Диагноз')),
                ('doctor', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='lk.Doctors', verbose_name='Доктор')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пациент')),
            ],
            options={
                'verbose_name': 'запись',
                'verbose_name_plural': 'Записи',
            },
        ),
        migrations.CreateModel(
            name='Notworkday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('not_work_day', models.DateField(blank=True, default=datetime.date(1, 1, 1), verbose_name='Нерабочие дни')),
                ('doctor', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='lk.Doctors', verbose_name='Доктор')),
            ],
            options={
                'verbose_name': 'нерабочий день',
                'verbose_name_plural': 'Нерабочие дни',
            },
        ),
    ]