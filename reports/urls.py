from django.urls import path

from . import views

urlpatterns = [
    path('report/<int:event_id>/edit_event', views.create_report, name='create_report'),
    path('report/<int:report_id>/report_profile', views.report_profile, name='report_profile'),
    path('report/<int:user_id>/scholarship_profile', views.scholarship_profile, name='scholarship_profile'),
    path('report/scholarship_list', views.scholarship_list, name='scholarship_list'),
    path('report/<int:user_id>/scholarship_delete', views.scholarship_delete, name='scholarship_delete'),
]
