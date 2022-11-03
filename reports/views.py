from pprint import pprint

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import CreateReportForm
from student.models import Event, Notification, Profile, AccessLevel

from student.views import required_login, create_notification, required_chief

from .models import EvaluateOrganizer, Report, Scholarship


@required_login
def create_report(request, event_id):
    event = Event.objects.get(id=event_id)
    part_list = event.part_list.all()
    print(part_list)
    if request.method == 'POST':
        form = CreateReportForm(request.POST)
        context = {
            'form': form,
            'title': 'Создание отчета',
            'event': event,
            'part_list': part_list,
            'notifications_list': Notification.objects.filter(profile=request.user).order_by('-id')
        }

        if form.is_valid():
            context['error'] = ''
            for profile in part_list:
                if request.POST[profile.username] is '' or int(request.POST[profile.username]) <= 0 or int(
                        request.POST[profile.username]) > 5:
                    context['error'] = 'Ошибка в выставлении баллов организаторам'
                    return render(request, 'create_report.html', context=context)
                if 'control_checkbox' not in request.POST:
                    context['error'] = 'Нет согласия об ответственности за составление отчета'
                    return render(request, 'create_report.html', context=context)
            pprint(request.POST)
            new_report = form.save()
            new_report.event = event
            new_report.save()
            for profile in part_list:
                new_evaluate = EvaluateOrganizer(report=new_report, profile=profile,
                                                 evaluate=int(request.POST[profile.username]))
                new_evaluate.save()
            create_notification(user=Profile.objects.get(access_level=AccessLevel.objects.get(name='Supervisor'),
                                                         direct=new_report.event.direct_event),
                                title='Отчет!',
                                content=f'Пользователь {request.user.username} отправил отчет '
                                        f'по мероприятию {new_report.event.name_event}')
            return HttpResponseRedirect(reverse('event_profile', args=[f'{event.id}']))
        else:
            return render(request, 'create_report.html', context=context)
    else:
        form = CreateReportForm()
        context = {
            'form': form,
            'title': 'Создание отчета',
            'event': event,
            'part_list': part_list,
            'notifications_list': Notification.objects.filter(profile=request.user).order_by('-id')
        }
        return render(request, 'create_report.html', context=context)


@required_login
def report_profile(request, report_id):
    report = Report.objects.get(id=report_id)
    evaluates = EvaluateOrganizer.objects.filter(report=report)
    if report.need_info:
        need_info = 'Да'
    else:
        need_info = 'Нет'

    if report.need_external:
        need_external = 'Да'
    else:
        need_external = 'Нет'

    context = {
        'title': f'Отчет {report.event.name_event}',
        'event': report.event,
        'report': report,
        'need_info': need_info,
        'need_external': need_external,
        'evaluates': evaluates,
        'notifications_list': Notification.objects.filter(profile=request.user).order_by('-id')
    }
    return render(request, 'report_profile.html', context=context)


@required_login
@required_chief
def scholarship_list(request):
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
        "title": "Список ПГАС",
        "notifications_list": Notification.objects.filter(profile=request.user).order_by('-id')
    }
    return render(request, 'scholarship_list.html', context=context)


@required_login
@required_chief
def scholarship_profile(request, user_id):
    user_evaluate = Profile.objects.get(id=user_id)
    if request.method == 'POST':
        own_score = 0
        for event in Event.objects.all():
            if event.name_event in request.POST:
                own_score += int(request.POST[event.name_event])
        obj = Scholarship(profile=user_evaluate, evaluate=own_score)
        obj.save()
        return HttpResponseRedirect(reverse('scholarship_list'))
    else:
        data = []
        count = 1
        for event in Event.objects.filter(main_organizer=user_evaluate):
            try:
                if event.status.name != 'Проведено' and not event.report:
                    continue
            except Exception:
                continue
            event_part = {'event': event.name_event, 'date': event.date_event, 'role': 'Главный организатор',
                          'score': EvaluateOrganizer.objects.filter(report=event.report).filter(
                              profile=user_evaluate)[0].evaluate}
            if event_part['score'] >= 3:
                event_part['approval'] = 'Да'
            else:
                event_part['approval'] = 'Нет'
            count += 1
            data.append(event_part.copy())
        for event in user_evaluate.part_list.all():
            try:
                if event.status.name != 'Проведено' and not event.report:
                    continue
            except Exception:
                continue
            repeat = False
            for item in data:
                if item['event'] == event.name_event:
                    repeat = True
                    break
            if repeat:
                continue
            event_part = {'event': event.name_event, 'date': event.date_event, 'role': 'Помощник главного организатора',
                          'score': EvaluateOrganizer.objects.filter(report=event.report).filter(
                              profile=user_evaluate)[0].evaluate}
            if event_part['score'] >= 3:
                event_part['approval'] = 'Да'
            else:
                event_part['approval'] = 'Нет'
            count += 1
            data.append(event_part.copy())
        pprint(data)
        context = {
            'data': data,
            'title': 'Оценивание ПГАС',
            'user_evaluate': user_evaluate,
            "notifications_list": Notification.objects.filter(profile=request.user).order_by('-id')
        }
        return render(request, 'scholarship_profile.html', context=context)


@required_login
@required_chief
def scholarship_delete(request, user_id):
    user_evaluate = Profile.objects.get(id=user_id)
    scholarship = user_evaluate.scholarship
    scholarship.delete()
    return HttpResponseRedirect(reverse('scholarship_list'))



