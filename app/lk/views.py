from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.http import JsonResponse
# сброс пароля
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
# stackoverflow.com/a/770078/63097
from django.db.models import Q
# доступ к вьюшке только залогиненому пользователю
from django.contrib.auth.decorators import login_required
from managment.models import Record, Notworkday
from .models import Doctors, Speciality


@login_required
def index(request):
    if request.POST:
        new_pass_form = PasswordChangeForm(
            user=request.user, data=request.POST)
        if new_pass_form.is_valid():
            new_pass_form.save()
            update_session_auth_hash(request, new_pass_form.user)
            return render(request, 'lk/lk-main.html', {
                'new_pass_form': new_pass_form,
                'succses_message': "Пароль успешно сменён"
            })
        return render(request, 'lk/lk-main.html', {'new_pass_form': new_pass_form})
    else:
        new_pass_form = PasswordChangeForm(user=request.user)
        return render(request, 'lk/lk-main.html', {'new_pass_form': new_pass_form})


@login_required
def history(request):
    recs = Record.objects.filter(user_id=request.user.id)
    filter_get = ""
    order_get = ""
    page_get = ""
    # Сортировка
    if "order" in request.GET:
        order_status = request.GET['order']
        order_get = '&order=' + order_status
        if order_status == '1':
            order_status = 'time'
        elif order_status == '-1':
            order_status = '-time'
        elif order_status == '2':
            order_status = 'doctor__specialty'
        elif order_status == '-2':
            order_status = '-doctor__specialty'
        elif order_status == '3':
            order_status = 'doctor__name'
        elif order_status == '-3':
            order_status = '-doctor__name'
        recs = recs.order_by(order_status)
        filter_text = "Все"
    else:
        recs = recs.order_by('-time')
        filter_text = "Все"

    # Фильтр
    if "filter" in request.GET:
        filter_status = request.GET['filter']
        filter_get = "&filter=" + filter_status
        if filter_status == '1':
            recs = recs.filter(status='Открыт')
            filter_text = 'Открытые'
        elif filter_status == '2':
            recs = recs.filter(status='Закрыт')
            filter_text = 'Закрытые'

    # Пагинация
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    paginator = Paginator(recs, 8)
    if "page" in request.GET:
        page = request.GET['page']
    else:
        page = "1"
    page_get = 'page=' + page
    try:
        recs = paginator.page(page)
    except PageNotAnInteger:
        # Если в гет передана не int.
        page = paginator.page(1)
    except EmptyPage:
        # Если число не верно.
        page = paginator.page(paginator.num_pages)

    args = {
        'records': recs,
        'filter_text': filter_text,
        'pg': page_get,
        'fg': filter_get,
        'og': order_get,
    }
    return render(request, 'lk/history.html', args)


@login_required
def annulment_record(request, id_record):
    """Отмена записи"""
    rec = Record.objects.get(id=id_record)
    rec.delete()
    return redirect('/lk/history/')
# -----------------------------------------------

# --------------record-------------------
# First step
@login_required
def specialists(request):
    specialitys = Speciality.objects.all()
    args = {'specialitys': specialitys}
    return render(request, 'lk/specialists.html', args)

# Second step or skip
@login_required
def choice_of_doctor(request, id_speciality):
    all_docs = Doctors.objects.filter(specialty__id=id_speciality)[:20]
    spec = Speciality.objects.get(id=id_speciality).speciality
    args = {'all_doctors': all_docs, 'speciality': spec}
    return render(request, 'lk/choice_of_doctor.html', args)

# final step
@login_required
def record(request, id_speciality, id_doctor):
    # доктор
    doctor = Doctors.objects.get(user__id=id_doctor)

    # подтягивание списка занятых ячеек
    busy_time_this_doctor = Record.objects.filter(doctor__user__id=id_doctor)
    busy_time_list = []

    for busy_time in busy_time_this_doctor:
        busy_time_list.append(busy_time.time)

    # --------------- запись пациента ------------------
    if request.GET:
        rec_date = request.GET['rec_date']
        rec_date = datetime.strptime(rec_date, r"%d-%m-%y-%H-%M")
        # записи пациента на сегодня к этому доктору
        today_recorded = Record.objects.filter(
            doctor__user__id=id_doctor,
            user=request.user,
            time__contains=rec_date.date()
        )

        if rec_date in busy_time_list:
            # занято
            return redirect('/lk/warning/?war=1')
        elif today_recorded:
            # сегодня уже записан
            return redirect('/lk/warning/?war=2')
        else:
            new_rec = Record()
            new_rec.doctor = doctor
            new_rec.user = request.user
            new_rec.time = rec_date
            new_rec.save()
            return redirect('/lk/history/')
    # --------------------------------------------------

    # текущяя дата +6 дней для шаблона
    now_plus_five = datetime.now() + timedelta(days=6)

    # шаг времени на 1 пациента
    time_step = doctor.schedule.time_step.minute
    # создание пустых листов
    days = {
        'day_1': [],
        'day_2': [],
        'day_3': [],
        'day_4': [],
        'day_5': [],
        'day_6': [],
        'day_7': []
    }
    one_weekday = []

    # создание обьектов datetime начала и конца приёма
    def get_work_time(num_weekday, status, the_date):
        if num_weekday == 1:
            if status == 'start':
                return datetime.combine(the_date, doctor.schedule.mo_start)
            if status == 'end':
                return datetime.combine(the_date, doctor.schedule.mo_end)
        if num_weekday == 2:
            if status == 'start':
                return datetime.combine(the_date, doctor.schedule.tu_start)
            if status == 'end':
                return datetime.combine(the_date, doctor.schedule.tu_end)
        if num_weekday == 3:
            if status == 'start':
                return datetime.combine(the_date, doctor.schedule.we_start)
            if status == 'end':
                return datetime.combine(the_date, doctor.schedule.we_end)
        if num_weekday == 4:
            if status == 'start':
                return datetime.combine(the_date, doctor.schedule.th_start)
            if status == 'end':
                return datetime.combine(the_date, doctor.schedule.th_end)
        if num_weekday == 5:
            if status == 'start':
                return datetime.combine(the_date, doctor.schedule.fr_start)
            if status == 'end':
                return datetime.combine(the_date, doctor.schedule.fr_end)

    def create_full_list(request, id_doctor):
        weekday = datetime.now().isoweekday()
        today = datetime.now().date()

        # ------ создание списка отменённых дней ------
        not_work_days_list = []
        not_work_days = Notworkday.objects.filter(doctor__user__id=id_doctor)
        for nwd in not_work_days:
            not_work_days_list.append(nwd.not_work_day)

        # 7 дней(от 1 до 9)

        for i in range(1, 8):
            start = get_work_time(weekday, 'start', today)
            end = get_work_time(weekday, 'end', today)

            # если не выходные и нет в списке отменённых дней, start.hour - в админке 0
            if start is not None and not today in not_work_days_list and start.hour:

                # основа
                while start <= end:
                    # распределение классов, проверка занятости
                    cel_class = ""
                    if start < datetime.now():
                        cel_class = "miss"
                    elif start in busy_time_list:
                        cel_class = "busy"
                    else:
                        cel_class = "free"

                    days['day_{}'.format(i)].append({
                        'time': start,
                        'class': cel_class
                    })
                    start += timedelta(minutes=time_step)

            # заполнение дня недели
            one_weekday.append(today)
            # сброс дня недели до понедельника
            weekday += 1
            if weekday == 8:
                weekday = 1

            today = today + timedelta(days=1)
            # print("Today:", today)

    create_full_list(request, id_doctor)

    from itertools import zip_longest
    timetbl = zip_longest(
        days['day_1'],
        days['day_2'],
        days['day_3'],
        days['day_4'],
        days['day_5'],
        days['day_6'],
        days['day_7']
    )
    args = {
        'doctor': doctor,
        'timetbl': timetbl,
        'one_weekday': one_weekday,
        'now_plus_five': now_plus_five
    }

    return render(request, 'lk/record.html', args)

# --------------schedule-------------------


def schedule_specialists(request):
    specialitys = Speciality.objects.all()
    args = {'specialitys': specialitys}
    return render(request, 'lk/specialists.html', args)

# Second step or skip


def schedule_choice_of_doctor(request, id_speciality):
    all_docs = Doctors.objects.filter(specialty__id=id_speciality)[:20]
    spec = Speciality.objects.get(id=id_speciality).speciality
    args = {'all_doctors': all_docs, 'speciality': spec}
    return render(request, 'lk/schedule_choice_of_doctor.html', args)

# final step


def schedule_record(request, id_speciality, id_doctor):
    doctor = Doctors.objects.get(user__id=id_doctor)
    start_add = []
    end_add = []
    start_add.append(doctor.schedule.mo_start)
    start_add.append(doctor.schedule.tu_start)
    start_add.append(doctor.schedule.we_start)
    start_add.append(doctor.schedule.th_start)
    start_add.append(doctor.schedule.fr_start)

    end_add.append(doctor.schedule.mo_end)
    end_add.append(doctor.schedule.tu_end)
    end_add.append(doctor.schedule.we_end)
    end_add.append(doctor.schedule.th_end)
    end_add.append(doctor.schedule.fr_end)

    # замена нулей на -
    counter = 0
    while counter < 5:
        if not start_add[counter].hour:
            start_add[counter] = '-'
        if not end_add[counter].hour:
            end_add[counter] = '-'
        counter += 1

    time_step = doctor.schedule.time_step.minute

    args = {
        'doctor': doctor,
        'start_add': start_add,
        'end_add': end_add,
        'time_step': time_step,
    }
    return render(request, 'lk/schedule.html', args)

# -----------------------------------------------


def warning(request):
    if request.GET:
        req = request.GET['war']
        error_msg = ""
        if req == '1':
            error_msg = "Выбранное время уже занято, попробуйто другое."
        if req == '2':
            error_msg = "На текущую к этому врачу у вас уже имеется запись."

        old_link = request.META['HTTP_REFERER'].split('/')
        old_link = '/' + '/'.join(old_link[3:])
        args = {
            'error_msg': error_msg,
            'old_link': old_link
        }
        return render(request, 'lk/warnings.html', args)
    else:
        return redirect('/lk/record/')


def doc_search(request):
    """Ajax search doctors"""
    if request.GET['term']:
        search = request.GET.get('term')
        result = []
        criterion1 = Q(name__icontains=search)
        criterion2 = Q(specialty__speciality__icontains=search)
        # https://stackoverflow.com/questions/27884129/django-queryset-foreign-key
        all_docs = Doctors.objects.filter(
            criterion1 | criterion2
        )[:20]
        for element in all_docs:
            speciality = element.specialty.speciality
            name = element.name
            label = "{} - {}".format(speciality, name)
            result.append({
                "doc_id": element.user.id,
                "doc_speciality_id": element.specialty.id,
                "label": label
            })
        return JsonResponse(result, safe=False)
    else:
        pass


def doc_profile(request, id_speciality, id_doctor):
    doctor = Doctors.objects.get(user__id=id_doctor)
    args = {'doctor': doctor}
    return render(request, 'lk/doc_profile.html', args)


def record_info(request):
    return render(request, 'lk/about_info.html')
