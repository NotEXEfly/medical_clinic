from django.shortcuts import render
from mysite.GLOBAL_VARS import SITE_NAME


def index(request):
    return render(request, 'mainApp/homepage.html', {"site_name": SITE_NAME})


def page404(request, exception):
    return render(request, 'main_page/404.html', {"message": "Message"})


def page500(request):
    return render(request, 'main_page/500.html', {"message": "Message"})
