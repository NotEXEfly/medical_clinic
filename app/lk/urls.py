from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('history/', views.history),
    path('history/<int:id_record>/', views.annulment_record),

    path('record/', views.specialists),
    path('record/<int:id_speciality>/', views.choice_of_doctor),
    path('record/<int:id_speciality>/<int:id_doctor>/timetable', views.record),
    path('record/<int:id_speciality>/<int:id_doctor>/info', views.doc_profile),

    path('schedule/', views.schedule_specialists),
    path('schedule/<int:id_speciality>/', views.schedule_choice_of_doctor),
    path('schedule/<int:id_speciality>/<int:id_doctor>/timetable',
         views.schedule_record),
    path('schedule/<int:id_speciality>/<int:id_doctor>/info', views.doc_profile),

    # подтягивание юрлов с managment
    path('', include('managment.urls')),

    path('info/', views.record_info),

    path('warning/', views.warning),
    # поиск врача Ajax
    path('doc_search/', views.doc_search),
]
