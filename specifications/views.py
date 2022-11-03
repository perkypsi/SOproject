from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from student.views import required_login, required_adm

from student.models import Notification, Profile, Direct

import os

from .forms import DocumentDownload
from .models import Document
from student.views import create_notification


@required_login
def rating(request):

    first = Profile.objects.all().order_by('rating')[0]
    second = Profile.objects.all().order_by('rating')[1]
    third = Profile.objects.all().order_by('rating')[2]
    all_direct = {}
    directs = [x for x in Direct.objects.all()]
    directs.remove(Direct.objects.get(short_name='АДМ'))
    for item in directs:
        all_direct[item.name] = Profile.objects.filter(direct=item).order_by('rating')[:10]
    context = {
        'title': 'Рейтинг СО',
        'all_direct': all_direct,
        'first': first,
        'second': second,
        'third': third,
        'notifications_list': Notification.objects.filter(profile=request.user).order_by('-id')
    }
    return render(request, 'rating.html', context=context)


@required_login
def documents(request):
    documentation = Document.objects.all()
    context = {
        'title': 'Документация',
        'documentation': documentation,
        'notifications_list': Notification.objects.filter(profile=request.user).order_by('-id')
    }
    return render(request, 'documents.html', context=context)


@required_login
@required_adm
def download_document(request):
    if request.method == 'POST':
        form = DocumentDownload(request.POST, request.FILES)
        context = {
            'form': form,
            'title': 'Загрузка документа',
            'notifications_list': Notification.objects.filter(profile=request.user).order_by('-id')
        }
        if form.is_valid():
            document = form.save()
            for user in Profile.objects.all():
                create_notification(user=user,
                                    title='Новый документ!',
                                    content=f'На сайте был загружен/обновлен документ "{document.name}" !')
            return HttpResponseRedirect(reverse('documents'))
        else:
            return render(request, 'download_document.html', context=context)
    else:
        form = DocumentDownload()
        context = {
            'form': form,
            'title': 'Загрузка документа',
            'notifications_list': Notification.objects.filter(profile=request.user).order_by('-id')
        }
        return render(request, 'download_document.html', context=context)


@required_login
@required_adm
def delete_document(request, document_id):
    document = Document.objects.get(id=document_id)
    os.remove(document.document.path)
    document.delete()
    return HttpResponseRedirect(reverse('documents'))