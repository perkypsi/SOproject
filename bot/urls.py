from django.urls import path
from . import views


urlpatterns = [
    path('bot/<int:secret_key>/login_request', views.login_request, name='login_request'),
    path('bot/<int:secret_key>/logout_request', views.logout_request, name='logout_request'),
]