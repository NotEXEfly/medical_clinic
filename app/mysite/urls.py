from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('mainApp.urls')),
    path('lk/', include('lk.urls')),
    path('admin/', admin.site.urls),
    # подтягивание юрлов с authentication
    path('', include('authentication.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'mainApp.views.page404'
handler500 = 'mainApp.views.page500'
