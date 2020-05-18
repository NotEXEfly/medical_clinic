from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth.models import User
from authentication.forms import RegUserForm, RegProfileForm
from mysite.GLOBAL_VARS import SITE_NAME


def login(request):
    '''Вход на сайт'''
    args = {}
    args['site_name'] = SITE_NAME
    if request.POST:
        u_name = request.POST['login'] or ''
        u_password = request.POST['password'] or ''
        user = auth.authenticate(username=u_name, password=u_password)
        if user is not None:
            auth.login(request, user)
            if request.user.is_staff:
                return redirect("/admin")
            else:
                return redirect("/lk/record/")
        else:
            args['log_error'] = "Логин или пароль введён неверно"
            return render(request, 'authentication/login.html', args)
    else:
        return render(request, 'authentication/login.html', args)


def logout(request):
    '''Выход с авторизации'''
    auth.logout(request)
    return redirect("/login")


def signup(request):
    '''Регистрация'''
    if request.POST:
        user_form = RegUserForm(request.POST)
        profile_form = RegProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            return redirect("/login")

        args = {'user_form': user_form,
                'profile_form': profile_form, 'site_name': SITE_NAME}
        return render(request, 'authentication/signup.html', args)
    else:
        user_form = RegUserForm()
        profile_form = RegProfileForm()

        args = {'user_form': user_form,
                'profile_form': profile_form, 'site_name': SITE_NAME}
        return render(request, 'authentication/signup.html', args)


def check_user_name(request):
    '''Ajax проверка занятости логина'''
    if request.GET:
        u_login = request.GET['u_login']
        # User.objects.values_list('username') - получить кортеж вида [(username,),(username,)]
        # User.objects.values('username') - получить словарь вида [{'username': 'username'}, {'username': 'username'}]
        if login_free(u_login):
            return HttpResponse('1')
        else:
            return HttpResponse('0')
    else:
        return redirect("/")


def login_free(u_login):
    '''Проверка занятости логина'''
    try:
        User.objects.get(username=u_login)
    except User.DoesNotExist:
        return False

    return True
