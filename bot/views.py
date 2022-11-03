from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view

from .models import Bot

from .config import SECRET_KEY


@api_view(['POST'])
def login_request(request, secret_key):
    if str(secret_key) != SECRET_KEY:
        return JsonResponse({'answer': 'no'})
    if request.method == 'POST':
        cleaned_data = {
            'username': request.POST['username'],
            'password': request.POST['password']
        }
        user = authenticate(request, **cleaned_data)
        if user is not None:
            try:
                user.bot.chat_id = request.POST['chat_id']
                user.bot.save()
            except Exception:
                obj = Bot(profile=user, chat_id=request.POST['chat_id'])
                obj.save()
            return JsonResponse({'answer': 'yes'})
        else:
            return JsonResponse({'answer': 'no'})
    else:
        return JsonResponse({'answer': 'no'})


@api_view(['POST'])
def logout_request(request, secret_key):
    if str(secret_key) != SECRET_KEY:
        return JsonResponse({'answer': 'no'})
    if request.method == 'POST':
        cleaned_data = {
            'username': request.POST['username'],
            'password': request.POST['password']
        }
        user = authenticate(request, **cleaned_data)
        if user is not None:
            try:
                user.bot.chat_id = None
                user.bot.save()
            except Exception:
                obj = Bot(profile=user, chat_id=None)
                obj.save()
            return JsonResponse({'answer': 'yes'})
        else:
            return JsonResponse({'answer': 'no'})
    else:
        return JsonResponse({'answer': 'no'})