from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login),
    # выход
    path('logout/', views.logout),

    path('checkUserName/', views.check_user_name),
]
