import datetime
import os
from wsgiref.util import FileWrapper

import requests as requests
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, path

import random
import csv
from transliterate import translit, get_available_language_codes

from .forms import CreateEventForm, LoginForm, EditEventForm, ProfileCreationForm, ProfileChangeForm
from .models import Event, Profile, StatusEvent, AccessLevel, Direct, Notification, Ban
from SOproject.settings import MEDIA_ROOT, MEDIA_URL

from bot.config import TOKEN_BOT


def required_chief(func):
    def wrapper(request, *args, **kwargs):
        if request.user.access_level != AccessLevel.objects.get(name='Chief'):
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return func(request, *args, **kwargs)

    return wrapper


def required_supervisor(func):
    def wrapper(request, *args, **kwargs):
        if request.user.access_level != AccessLevel.objects.get(name='Supervisor'):
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return func(request, *args, **kwargs)

    return wrapper


def required_adm(func):
    def wrapper(request, *args, **kwargs):
        if request.user.access_level != AccessLevel.objects.get(name='Chief') and \
                request.user.access_level != AccessLevel.objects.get(name='Administrator'):
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return func(request, *args, **kwargs)

    return wrapper


def required_login(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        else:
            try:
                if request.user.ban:
                    return HttpResponseRedirect(reverse('ban_page', args=(request.user.ban.id,)))
            except Exception:
                pass
            if request.user.last_visit != datetime.date.today():
                request.user.last_visit = datetime.date.today()
                request.user.save()
            return func(request, *args, **kwargs)

    return wrapper


def update_deadline():
    all_events = Event.objects.filter(status__name='Реализация')
    for event in all_events:
        if event.date_event is None:
            continue
        if event.date_event < datetime.date.today():
            event.status = StatusEvent.objects.get(name='Проведено')
            event.save()
            create_notification(user=event.main_organizer,
                                title='Сдайте отчет!',
                                content=f'Ваше мероприятие "{event.name_event}" завершено. '
                                        f'Пожалуйста, сдайте отчет по мероприятию. Это можно сделать на основной '
                                        f'странице мероприятия.')


def update_score_users():
    for user in Profile.objects.all():
        own_event_list = Event.objects.filter(main_organizer=user)
        amount_assistants = -own_event_list.count()
        for event in own_event_list:
            amount_assistants += event.part_list.count()
        assistant_in_events = user.part_list.count() - own_event_list.count()
        user.rating_score = own_event_list.count() * 6 + amount_assistants * 2 + assistant_in_events * 4
        user.save()


def update_rating():
    users_list = Profile.objects.order_by('-rating_score')
    for i in range(len(users_list)):
        users_list[i].rating = i + 1
        users_list[i].save()


def update_all(request):
    update_deadline()
    update_score_users()
    update_rating()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@required_login
def create_review(request):
    if request.method == 'POST':
        author = request.user.username
        title = request.POST['title']
        content = request.POST['content']
        message = f"Автор: {author}\nПредложение/ошибка: {title}\nСодержание: {content}\n"
        print(message)
        requests.get(
            f'https://api.telegram.org/bot5562647811:AAEkzgi-BtgRR_L3Mj4YtqXBMHafq3boJ_Y/sendMessage?chat_id=463762417&text={message}')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def create_notification(user, title, content):
    note = Notification.objects.create(title=title,
                                       content=content,
                                       profile=user)
    note.save()
    message = f"{title}\n{content}\n"
    try:
        requests.get(f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage?chat_id={user.bot.chat_id}&text={message}")
    except Exception:
        pass


@required_login
def home(request):
    update_deadline()
    update_rating()
    own_event_list = Event.objects.filter(main_organizer=request.user)
    audience_reach = sum([int(event.amount_participants) for event in own_event_list])
    amount_assistants = -own_event_list.count()
    for event in own_event_list:
        amount_assistants += event.part_list.count()
    assistant_in_events = request.user.part_list.count() - own_event_list.count()
    specifications_list_info = Event.objects.filter(
        Q(need_info=True) & (Q(status__name='Реализация') | Q(status__name='Рассмотрение')))
    specifications_list_external = Event.objects.filter(
        Q(need_external=True) & (Q(status__name='Реализация') | Q(status__name='Рассмотрение')))
    queue_list = {}
    for own_event in own_event_list:
        queue_list[own_event] = own_event.queue_list.all()
    applications_for_approval = Event.objects.filter(
        Q(status__name='Регистрация') | Q(status__name='Рассмотрение'))

    context = {
        'own_event_list': own_event_list.order_by('-id'),
        'queue_list': queue_list,
        'applications_for_approval': applications_for_approval,
        'audience_reach': audience_reach,
        'amount_assistants': amount_assistants,
        'specifications_list_info': specifications_list_info,
        'specifications_list_external': specifications_list_external,
        'assistant_in_events': assistant_in_events,
        'title': 'Главная',
        'notifications_list': Notification.objects.filter(profile=request.user).order_by('-id')
    }
    return render(request, 'home.html', context=context)


@required_login
def events(request):
    search_query = request.GET.get('search', '')
    events_list = Event.objects.order_by('-id')
    if search_query:
        events_list = events_list.filter(Q(name_event__icontains=search_query)
                                         | Q(direct_event__name__icontains=search_query)
                                         | Q(status__name__icontains=search_query)
                                         | Q(concept_event__icontains=search_query))
    context = {
        "events_list": events_list,
        "title": "Список мероприятий",
        "notifications_list": Notification.objects.filter(profile=request.user).order_by('-id')
    }
    return render(request, 'activity.html', context=context)


@required_login
def event_profile(request, event_id):
    event = Event.objects.get(id=event_id)
    part_list = event.part_list.all()
    queue_list = event.queue_list.all()
    deadline_info_off = False
    deadline_external_off = False
    context = {
        'profiles': Profile.objects.all(),
        'event': event,
        'part_list': part_list,
        'queue_list': queue_list,
        'datetime': datetime,
        'deadline_info_off': deadline_info_off,
        'deadline_external_off': deadline_external_off,
        'title': event.name_event,
        'notifications_list': Notification.objects.filter(profile=request.user).order_by('-id')
    }
    if event.main_organizer == request.user:
        return render(request, 'event_profile_master.html', context=context)
    else:
        return render(request, 'event_profile_guest.html', context=context)


@required_login
def profile(request, user_id):
    profile_instance = Profile.objects.get(id=user_id)
    if request.user == profile_instance:
        attributes_list = {
            "Соц. сеть": profile_instance.link_social,
            "Комитет": profile_instance.direct,
            "Уровень доступа": profile_instance.access_level,
            "Учебная группа": profile_instance.edu_group,
            "Телефонный номер": profile_instance.phone_number,
            "Email": profile_instance.email,
            "Дата рождения": profile_instance.birthdate,
            "Должность": profile_instance.post
        }
    elif request.user.access_level == AccessLevel.objects.get(name='Participant'):
        if (profile_instance.access_level == request.user.access_level or
            profile_instance.access_level == AccessLevel.objects.get(name='Supervisor')) and \
                profile_instance.direct == request.user.direct:
            attributes_list = {
                "Соц. сеть": profile_instance.link_social,
                "Комитет": profile_instance.direct,
                "Дата рождения": profile_instance.birthdate,
                "Должность": profile_instance.post
            }
        else:
            return HttpResponseRedirect(reverse('home'))
    else:
        attributes_list = {
            "Соц. сеть": profile_instance.link_social,
            "Комитет": profile_instance.direct,
            "Уровень доступа": profile_instance.access_level,
            "Учебная группа": profile_instance.edu_group,
            "Телефонный номер": profile_instance.phone_number,
            "Email": profile_instance.email,
            "Дата рождения": profile_instance.birthdate,
            "Должность": profile_instance.post
        }
    context = {
        "profile": profile_instance,
        "attributes_list": attributes_list,
        "title": "Профиль",
        "notifications_list": Notification.objects.filter(profile=request.user).order_by('-id')

    }
    return render(request, 'profile.html', context=context)


@required_login
def users(request):
    search_query = request.GET.get('search', '')
    if request.user.access_level == AccessLevel.objects.get(name='Participant'):
        list_users = Profile.objects.filter(Q(access_level=AccessLevel.objects.get(name='Participant'))
                                            & Q(direct=request.user.direct))
    else:
        list_users = Profile.objects.order_by('id')
    if search_query:
        list_users = list_users.filter(Q(username__icontains=search_query)
                                       | Q(direct__name__icontains=search_query)
                                       | Q(access_level__name__icontains=search_query)
                                       | Q(last_name__icontains=search_query)
                                       | Q(first_name__icontains=search_query)
                                       | Q(post__icontains=search_query))
    paginator = Paginator(list_users, 15)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "list_users": list_users,
        "search_query": search_query,
        "chief": AccessLevel.objects.get(name='Chief'),
        "notifications_list": Notification.objects.filter(profile=request.user).order_by('-id')
    }
    return render(request, 'list_members.html', context=context)


def login_profile(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                form.add_error(None, "Неверный логин или пароль")
    else:
        if request.user is not None:
            logout(request)
        form = LoginForm()
    return render(request, 'auth.html', {"form": form})


@required_login
def create_event(request):
    if request.method == 'POST':
        form = CreateEventForm(request.POST)
        context = {
            'form': form,
            'title': 'Создание мероприятия',
            'notifications_list': Notification.objects.filter(profile=request.user).order_by('-id')
        }
        if form.is_valid():
            print(form.cleaned_data)
            new_event = form.save()
            new_event.main_organizer = request.user
            new_event.name_author = request.user.last_name + ' ' + request.user.first_name + ' ' + request.user.patronymic
            new_event.email_author = request.user.email
            new_event.phone_author = request.user.phone_number
            new_event.part_list.add(request.user)
            new_event.status = StatusEvent.objects.get(name="Регистрация")
            new_event.save()
            create_notification(user=Profile.objects.get(access_level=AccessLevel.objects.get(name='Supervisor'),
                                                         direct=new_event.direct_event),
                                title='Новое мероприятие!',
                                content=f'Пользователь {request.user.username} отправил заявку '
                                        f'на регистрацию нового мероприятия {new_event.name_event}')
            return HttpResponseRedirect(reverse('activity'))
        else:
            return render(request, 'create_event.html', context=context)
    else:
        form = CreateEventForm()
        context = {
            'form': form,
            'title': 'Создание мероприятия',
            'notifications_list': Notification.objects.filter(profile=request.user).order_by('-id')
        }
        return render(request, 'create_event.html', context=context)


@required_login
def edit_event(request, event_id):
    event = Event.objects.get(id=event_id)

    if request.method == 'POST':
        form = EditEventForm(request.POST, instance=event)
        context = {
            'form': form,
            'title': 'Редактирование мероприятия',
            'event': event,
            'notifications_list': Notification.objects.filter(profile=request.user).order_by('-id')
        }
        if form.is_valid():
            new_event = form.save()
            return HttpResponseRedirect(reverse('event_profile', args=(event_id,)))
        else:
            return render(request, 'edit_event.html', context=context)

    else:
        form = EditEventForm(instance=event)
        context = {
            'form': form,
            'title': 'Редактирование мероприятия',
            'event': event,
            'notifications_list': Notification.objects.filter(profile=request.user).order_by('-id')
        }
        return render(request, 'edit_event.html', context=context)


@required_login
def cancel_event(request, event_id):
    event = Event.objects.get(id=event_id)
    user = event.main_organizer
    user.rating_score -= 6
    user.save()
    create_notification(user=user,
                        title='Отмена мероприятия',
                        content=f'Администратор отменил ваше мероприятие "{event.name_event}"')
    event.delete()

    return HttpResponseRedirect(reverse('activity'))


@required_login
def delete_user_from_event(request, event_id, user_id):
    event = Event.objects.get(id=event_id)
    participant = Profile.objects.get(id=user_id)
    participant.rating_score -= 4
    participant.save()
    user = request.user
    user.rating_score -= 2
    user.save()
    event.part_list.remove(participant)
    create_notification(user=user,
                        title='Больше не помощник организатора(',
                        content=f'Вы больше не участвуете в помощи в организации мероприятия '
                                f'"{event.name_event}"')
    return HttpResponseRedirect(reverse('event_profile', args=(event_id,)))


@required_login
def register_user_activity(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except:
        raise Http404("Мероприятие не найдено!")
    event.queue_list.add(request.user)
    create_notification(user=event.main_organizer,
                        title='Новый помощник организатора',
                        content=f'"{request.user.username}" хочет помочь в организации вашего мероприятия '
                                f'"{event.name_event}"')
    return HttpResponseRedirect(reverse('event_profile', args=(event_id,)))


@required_login
def confirm_register_users(request, event_id, user_id):
    try:
        event = Event.objects.get(id=event_id)
    except:
        raise Http404("Мероприятие не найдено!")

    user = Profile.objects.get(id=user_id)
    event.queue_list.remove(user)
    event.part_list.add(user)
    user.rating_score += 4
    user.save()
    request.user.rating_score += 2
    request.user.save()
    create_notification(user=request.user,
                        title='Приняли в мероприятие!',
                        content=f'Главный организатор одобрил вашу заявку на помощь в организации мероприятия '
                                f'"{event.name_event}"')
    return HttpResponseRedirect(reverse('home'))


@required_login
def cancel_register_users(request, event_id, user_id):
    try:
        event = Event.objects.get(id=event_id)
    except:
        raise Http404("Мероприятие не найдено!")

    user = Profile.objects.get(id=user_id)
    event.queue_list.remove(user)
    create_notification(user=user,
                        title='Вас не приняли(',
                        content=f'Главный организатор отклонил вашу заявку на помощь в организации мероприятия '
                                f'"{event.name_event}"')
    return HttpResponseRedirect(reverse('home'))


@required_login
def approval_event(request, event_id):
    event = Event.objects.get(id=event_id)
    if event.status.name == "Регистрация":
        event.status = StatusEvent.objects.get(name='Разработка')
        event.main_organizer.rating_score += 6
        event.main_organizer.save()
        create_notification(user=event.main_organizer,
                            title='Одобрено!',
                            content=f'Ваше мероприятие "{event.name_event}" имеет новый статус "Разработка"')
    elif event.status.name == "Рассмотрение":
        if request.user.access_level == AccessLevel.objects.get(name='Supervisor') and \
                request.user.direct == event.direct_event:
            event.project_documentation = True
        if request.user.access_level == AccessLevel.objects.get(name='Supervisor') and \
                request.user.direct == Direct.objects.get(id_name='info'):
            event.info_documentation = True
        if request.user.access_level == AccessLevel.objects.get(name='Supervisor') and \
                request.user.direct == Direct.objects.get(id_name='external'):
            event.external_documentation = True

        if event.project_documentation and (not (event.need_info ^ event.info_documentation) and not (
                event.need_external ^ event.external_documentation)):
            event.status = StatusEvent.objects.get(name='Реализация')
            create_notification(user=event.main_organizer,
                                title='Одобрено!',
                                content=f'Ваше мероприятие "{event.name_event}" имеет новый статус "Реализация"')
    event.save()
    return HttpResponseRedirect(reverse('home'))


@required_login
def degradation_status(request, event_id):
    event = Event.objects.get(id=event_id)
    if event.status.name == "Регистрация":
        create_notification(user=event.main_organizer,
                            title='Отклонено(',
                            content=f'Ваше мероприятие "{event.name_event}" не было одобрено')
        event.delete()
    elif event.status.name == "Рассмотрение":
        event.status = StatusEvent.objects.get(name='Разработка')
        event.save()
        create_notification(user=event.main_organizer,
                            title='Отклонено(',
                            content=f'Ваше мероприятие "{event.name_event}" не было одобрено, необходима доработка!')
    return HttpResponseRedirect(reverse('home'))


@required_login
def ending_event(request, event_id):
    event = Event.objects.get(id=event_id)
    if event.status.name == "Разработка":
        if event.need_info:
            if event.date_event - datetime.timedelta(days=17) < datetime.date.today():
                event.need_info = False
            create_notification(user=Profile.objects.get(access_level=AccessLevel.objects.get(name='Supervisor'),
                                                         direct=Direct.objects.get(id_name='info')),
                                title='Новое ТЗ',
                                content=f'У мероприятия "{event.name_event}" появилось ТЗ!')
        if event.need_external:
            if event.date_event - datetime.timedelta(days=24) < datetime.date.today():
                event.need_external = False
                create_notification(user=Profile.objects.get(access_level=AccessLevel.objects.get(name='Supervisor'),
                                                             direct=Direct.objects.get(
                                                                 id_name='external')),
                                    title='Новое ТЗ',
                                    content=f'У мероприятия "{event.name_event}" появилось ТЗ!')
        event.status = StatusEvent.objects.get(name='Рассмотрение')
    event.save()
    create_notification(user=Profile.objects.get(access_level=AccessLevel.objects.get(name='Supervisor'),
                                                 direct=event.direct_event),
                        title='Заявка на реализацию',
                        content=f'Пользователь {request.user.username} отправил заявку '
                                f'на реализацию мероприятия {event.name_event}')
    return HttpResponseRedirect(reverse('event_profile', args=(event_id,)))


@required_login
def add_mendeleev_bonus(request, event_id):
    event = Event.objects.get(id=event_id)
    event.mendeleev_bonus = True
    event.save()
    return redirect('https://vk.com/away.php?to=https%3A%2F%2Fforms.gle%2F9MLx1uxJwf4PcSS89')


@required_login
@required_supervisor
def change_main_organizer(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        latest_main_organizer = event.main_organizer
        user_change = request.POST['login']
        event.main_organizer = Profile.objects.get(id=user_change)
        event.part_list.add(Profile.objects.get(id=user_change))
        event.save()
        create_notification(user=Profile.objects.get(id=user_change),
                            title='Ты главный организатор!',
                            content=f'Руководитель назначил тебя главным организатором мероприятия '
                                    f'"{event.name_event}"')
        create_notification(user=latest_main_organizer,
                            title='Смена главного организатора',
                            content=f'Руководитель снял тебя с должности главного организатора мероприятия '
                                    f'"{event.name_event}"')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@required_login
def delete_notification(request, user_id):
    user = Profile.objects.get(id=user_id)
    for notification in user.notification_set.all():
        notification.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def download_word_pp(request, event_id):
    from docxtpl import DocxTemplate

    doc = DocxTemplate(MEDIA_ROOT + "/templates/project_map_template.docx")
    event_super = Event.objects.get(id=event_id)
    part_list = [x for x in event_super.part_list.all()]
    part_list.remove(event_super.main_organizer)
    context_1 = {
        'event': event_super,
        'part_list': part_list
    }
    doc.render(context_1)
    doc.save(MEDIA_ROOT + f"/results/project_{event_super.id}.docx")

    return redirect(MEDIA_URL+f'/results/project_{event_super.id}.docx')



@required_login
@required_adm
def adm_panel(request):
    all_users = Profile.objects.count()
    all_events = Event.objects.count()

    active_users = 0
    main_organizer_users = 0
    amount_visits = 0

    amount_into_direct = {}
    amount_into_direct_percent = {}

    for direction in Direct.objects.all():
        amount_into_direct[direction.short_name] = 0

    for user in Profile.objects.all():
        amount_into_direct[user.direct.short_name] += 1
        if user.part_list.count() != 0:
            active_users += 1
            if user.main_event.count() != 0:
                main_organizer_users += 1
            else:
                print(user.last_visit)
        if datetime.date.today() - user.last_visit < datetime.timedelta(days=7):
            amount_visits += 1

    for direct, amount in amount_into_direct.items():
        amount_into_direct_percent[direct] = round(amount * 100 / all_users)

    events_list = {
        'Регистрация': Event.objects.filter(status__name='Регистрация').count(),
        'Разработка': Event.objects.filter(status__name='Разработка').count(),
        'Рассмотрение': Event.objects.filter(status__name='Рассмотрение').count(),
        'Реализация': Event.objects.filter(status__name='Реализация').count(),
        'Проведено': Event.objects.filter(status__name='Проведено').count(),
    }

    context = {
        'active_users': round(active_users * 100 / all_users),
        'main_organizer_users': round(main_organizer_users * 100 / all_users),
        'amount_visits': round(amount_visits * 100 / all_users, 2),
        'amount_visits_round': round(amount_visits * 100 / all_users),
        'all_users': all_users,
        'events_list': events_list,
        'amount_into_direct': amount_into_direct,
        'all_events': all_events,
        'amount_into_direct_percent': amount_into_direct_percent,
        'notifications_list': Notification.objects.filter(profile=request.user).order_by('-id')
    }

    return render(request, 'adm_panel.html', context=context)


@required_login
@required_chief
def delete_user(request, user_id):
    user = Profile.objects.get(id=user_id)
    user.delete()
    return HttpResponseRedirect(reverse('users'))


@required_login
@required_chief
def edit_user(request, user_id):
    user = Profile.objects.get(id=user_id)
    if request.method == 'POST':
        form = ProfileChangeForm(request.POST, instance=user)
        context = {
            'form': form,
            'title': 'Редактирование пользователя',
            'user_id': user.id,
            'notifications_list': Notification.objects.filter(profile=request.user).order_by('-id')
        }
        if form.is_valid():
            new_user = form.save()
            create_notification(user=new_user,
                                title='Параметры пользователя',
                                content=f'Внимание! Администратор изменил твои параметры пользователя! '
                                        f'Проверь еще раз информацию в профиле. '
                                        f'В случае ошибки, свяжись с председателем Совета Обучающихся')
            return HttpResponseRedirect(reverse('users'))
        else:
            return render(request, 'edit_profile.html', context=context)
    else:
        form = ProfileChangeForm(instance=user)
        context = {
            'form': form,
            'title': 'Редактирование пользователя',
            'user_id': user.id,
            'notifications_list': Notification.objects.filter(profile=request.user).order_by('-id')
        }
        return render(request, 'edit_profile.html', context=context)


@required_login
@required_chief
def create_user(request):
    if request.method == 'POST':
        form = ProfileCreationForm(request.POST)
        context = {
            'form': form,
            'title': 'Создание пользователя',
            'notifications_list': Notification.objects.filter(profile=request.user).order_by('-id')
        }
        if form.is_valid():
            new_user = form.save()
            new_user.rating_score = 0
            new_user.last_visit = datetime.datetime.strptime(f'01 01 2001', '%d %m %Y')
            new_user.save()
            create_notification(user=new_user,
                                title='Добро пожаловать!',
                                content=f'Рады приветствовать в нашей семье!\n'
                                        f'Инструкции по использованию рабочей среды (сайта) '
                                        f'ты получишь у своего руководителя комитеты.\nУдачи!')
            return HttpResponseRedirect(reverse('adm_panel'))
        else:
            return render(request, 'create_profile.html', context=context)
    else:
        form = ProfileCreationForm()
        context = {
            'form': form,
            'title': 'Создание пользователя',
            'notifications_list': Notification.objects.filter(profile=request.user).order_by('-id')
        }
        return render(request, 'create_profile.html', context=context)


@required_login
@required_adm
def ban_user(request, user_id):
    if request.method == 'POST':
        date = request.POST['hours']
        if not date.isdigit():
            date = 1
        elif int(date) <= 0:
            date = 1
        profile_ban = Profile.objects.get(id=user_id)
        if profile_ban.access_level.name == 'Administrator' or \
                profile_ban.access_level.name == 'Chief':
            HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        date_ban = datetime.datetime.now() + datetime.timedelta(hours=date)
        ban = Ban(profile=profile_ban, datetime=date_ban)
        ban.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@required_login
@required_adm
def unban_user(request, user_id):
    profile_ban = Profile.objects.get(id=user_id)
    ban = profile_ban.ban
    ban.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def ban_page(request, ban_id):
    ban = Ban.objects.get(id=ban_id)
    context = {
        'date': ban.datetime
    }
    return render(request, 'ban.html', context=context)


@required_login
@required_adm
def parsing_users(request):
    def password_generator():
        chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_'
        password = ''
        for j in range(4):
            for i in range(3):
                password += random.choice(chars)
            if j != 3:
                password += '-'
        return password

    users_parsing = []

    file = open(MEDIA_ROOT + 'data.txt', mode='w')
    file.write(f'LOGIN          PASSWORD       \n')
    file.close()

    with open(MEDIA_ROOT + 'members_so.csv', mode='r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        for row in reader:
            if "Фамилия Имя Отчество" in row:
                continue
            users_parsing.append(row)

    for user in users_parsing:
        full_name = user[0].split()
        password = password_generator()
        username = (translit(f"{full_name[1][0]}", 'ru', reversed=True) + translit(f"{full_name[0]}", 'ru',
                                                                                   reversed=True)).lower()

        obj = Profile.objects.create_user(username=username,
                                          first_name=full_name[1],
                                          last_name=full_name[0],
                                          patronymic=full_name[2],
                                          password=password,
                                          edu_group=user[1],
                                          phone_number=int(user[2]),
                                          link_social=user[3],
                                          email=user[4],
                                          birthdate=datetime.datetime.strptime(
                                              f'{user[5]}',
                                              '%d.%m.%Y'),
                                          post=user[6],
                                          direct=Direct.objects.get(name=user[7]),
                                          access_level=AccessLevel.objects.get(name=user[8]),
                                          rating_score=0,
                                          last_visit=datetime.datetime.strptime(
                                              f'{random.randint(1, 22)} 10 2022', '%d %m %Y'))
        obj.save()
        create_notification(user=obj,
                            title='Добро пожаловать!',
                            content=f'Рады приветствовать в нашей семье!\n'
                                    f'Инструкции по использованию рабочей среды (сайта) '
                                    f'ты получишь у своего руководителя комитеты.\nУдачи!')
        print(f"Создался {user}")
        file = open('student/data.txt', mode='a')
        file.write(f'{username:<15}{password:<16}---> OK\n')
        file.close()

    return HttpResponseRedirect(reverse('adm_panel'))


def test_delete_users(request):
    all = set()

    with open('student/tst.txt', mode='r', encoding='utf-8') as file:
        for line in file.readlines():
            all.add(line[:-1].lower())

    users_list = [Profile.objects.get(username=x) for x in all]
    for user in users_list:
        user.delete()
    return HttpResponseRedirect(reverse('adm_panel'))


def test_create_events(request):
    count_events = 200
    for i in range(count_events):
        name = f'Event {i}'
        aims = f'Aims of event {i}'
        concept = f'Concept of event {i}'
        place = f'Place of event {i}'
        days = [x for x in range(1, 29)]
        months = [x for x in range(1, 13)]
        years = [x for x in range(2021, 2023)]
        random_status = random.choice(StatusEvent.objects.all())
        users_list = [user for user in Profile.objects.all()]
        mg = random.choice(users_list)
        users_list.remove(mg)
        participant_list = []
        queue_list = []
        if random_status.name == 'Регистрация':
            pass
        elif random_status.name == 'Разработка':
            for user_part in range(random.randint(3, 8)):
                random_user = random.choice(users_list)
                participant_list.append(random_user)
                users_list.remove(random_user)
            for user_queue in range(random.randint(3, 8)):
                random_user = random.choice(users_list)
                queue_list.append(random_user)
                users_list.remove(random_user)
        elif random_status.name == 'Рассмотрение':
            for user_part in range(random.randint(3, 8)):
                random_user = random.choice(users_list)
                participant_list.append(random_user)
                users_list.remove(random_user)
        elif random_status.name == 'Реализация':
            for user_part in range(random.randint(3, 8)):
                random_user = random.choice(users_list)
                participant_list.append(random_user)
                users_list.remove(random_user)
        elif random_status.name == 'Проведено':
            for user_part in range(random.randint(3, 8)):
                random_user = random.choice(users_list)
                participant_list.append(random_user)
                users_list.remove(random_user)

        obj = Event.objects.create(name_event=name,
                                   direct_event=random.choice(Direct.objects.all()),
                                   aims_event=aims,
                                   concept_event=concept,
                                   amount_participants=random.randint(10, 1000),
                                   place_event=place,
                                   status=random.choice(StatusEvent.objects.all()),
                                   main_organizer=mg,
                                   date_event=datetime.datetime.strptime(
                                       f'{random.choice(days)} {random.choice(months)} {random.choice(years)}',
                                       '%d %m %Y')
                                   )
        obj.part_list.add(mg)
        for user in participant_list:
            obj.part_list.add(user)
        for user in queue_list:
            obj.queue_list.add(user)
        obj.save()
        print(f"Создано {i} мероприятие")

    return HttpResponseRedirect(reverse('adm_panel'))


def test_delete_events(request):
    all_events = Event.objects.all()
    for event in all_events:
        event.delete()
    return HttpResponseRedirect(reverse('adm_panel'))
