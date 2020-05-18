from django.contrib import admin
from authentication.models import Profile
# Register your models here.

# вывод в админке
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'fio', 'avatar')

    def user_info(self, obj):
        return obj.user


admin.site.register(Profile, ProfileAdmin)
