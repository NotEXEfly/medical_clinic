from django.contrib import admin
from lk.models import Doctors, Speciality, Schedule


class DoctorsAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'start_day_work', 'end_day_work')

    def user_info(self, obj):
        return obj.user


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor',)


admin.site.register(Doctors, DoctorsAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Speciality)
