from datetime import datetime, timedelta
from django.contrib import admin
from managment.models import Record, Notworkday, Contact
from lk.models import Doctors


class DateListFilter(admin.SimpleListFilter):
    '''Фильтр по дате'''

    title = ('По дате')
    parameter_name = 'date'

    def lookups(self, request, model_admin):
        return (
            ('today', ('Сегодня')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'today':
            before = datetime.now().date()
            after = datetime.now().date() + timedelta(days=1)
            return queryset.filter(time__gte=before).filter(time__lte=after)


class StatusListFilter(admin.SimpleListFilter):
    '''Фильтр по статусу'''

    title = ('По статусу')
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('open', ('Открыт')),
            ('close', ('Закрыт')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'open':
            return queryset.filter(status="Открыт")

        if self.value() == 'close':
            return queryset.filter(status="Закрыт")


class RecordAdmin(admin.ModelAdmin):

    readonly_fields = ('user', 'doctor', 'time')
    list_display = ('fio_user', 'time', 'status')

    # поиск по полю
    search_fields = ('user__profile__fio',)

    # Фильтр
    list_filter = (DateListFilter, StatusListFilter)
    # вывод фио пользователя в админке

    def fio_user(self, obj):
        return obj.user.profile.fio
    fio_user.short_description = 'Пациент'
    # на чём сслыка стоит
    # list_display_links = ('doctor_id',)

    # вывод врачам своих пациентов
    def get_queryset(self, request):
        qs = super(RecordAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(doctor_id=request.user.id)


class NotworkdayAdmin(admin.ModelAdmin):

    list_display = ('doctor', 'not_work_day')

    # автоматический выбор текущего врчача и нельзя сменить
    raw_id_fields = ('doctor',)
    readonly_fields = ('doctor',)

    # возможность врачам редактировать только свои выходные
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'doctor' and not request.user.is_superuser:
            kwargs["queryset"] = Doctors.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # вывод только выходных текущего врача
    def get_queryset(self, request):
        qs = super(NotworkdayAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(doctor_id=request.user.id)


class ContactAdmin(admin.ModelAdmin):
    readonly_fields = ('subject', 'message', 'sender', 'answered')
    list_display = ('subject', 'sender', 'send', 'answered')

    # запретить редактирование когда сообщение уже отправленно
    def get_readonly_fields(self, request, obj):
        if obj.answered:
            return ('subject', 'message', 'sender', 'send', 'answer', 'answered')

        return self.readonly_fields


admin.site.register(Record, RecordAdmin)
admin.site.register(Notworkday, NotworkdayAdmin)
admin.site.register(Contact, ContactAdmin)
