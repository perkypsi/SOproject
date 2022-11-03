from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events', views.events, name='events'),
    path('users', views.users, name='users'),
    path('adm_panel', views.adm_panel, name='adm_panel'),
    path('<int:event_id>/event_profile', views.event_profile, name='event_profile'),
    path('<int:user_id>/profile', views.profile, name='profile'),
    path('create_event', views.create_event, name='create_event'),
    path('<int:event_id>/edit_event', views.edit_event, name='edit_event'),
    path('<int:event_id>/cancel_event', views.cancel_event, name='cancel_event'),
    path('<int:event_id>/<int:user_id>/delete_user_from_event', views.delete_user_from_event,
         name='delete_user_from_event'),
    path('<int:event_id>/register_user_activity', views.register_user_activity,
         name='register_user_activity'),
    path('<int:event_id>/<int:user_id>/confirm_register_users', views.confirm_register_users,
         name='confirm_register_users'),
    path('<int:event_id>/<int:user_id>/cancel_register_users', views.cancel_register_users,
         name='cancel_register_users'),
    path('<int:event_id>/approval_event', views.approval_event,
         name='approval_event'),
    path('<int:event_id>/degradation_status', views.degradation_status,
         name='degradation_status'),
    path('<int:event_id>/ending_event', views.ending_event, name='ending_event'),
    path('<int:event_id>/add_mendeleev_bonus', views.add_mendeleev_bonus, name='add_mendeleev_bonus'),
    path('<int:event_id>/change_main_organizer', views.change_main_organizer, name='change_main_organizer'),
    path('<int:event_id>/download_word_pp', views.download_word_pp, name='download_word_pp'),
    path('<int:user_id>/delete_notification', views.delete_notification, name='delete_notification'),
    path('auth', views.login_profile, name='login'),
    path('create_user', views.create_user, name='create_user'),
    path('<int:user_id>/edit_user', views.edit_user, name='edit_user'),
    path('<int:user_id>/delete_user', views.delete_user, name='delete_user'),

    path('parsing_users', views.parsing_users, name='parsing_users'),
    path('test_delete_users', views.test_delete_users, name='test_delete_users'),
    path('test_create_events', views.test_create_events, name='test_create_events'),
    path('test_delete_events', views.test_delete_events, name='test_delete_events'),
    path('update_all', views.update_all, name='update_all'),
    path('review', views.create_review, name='review'),
    path('<int:ban_id>/ban_page', views.ban_page, name='ban_page'),
    path('<int:user_id>/ban_user', views.ban_user, name='ban_user'),
    path('<int:user_id>/unban_user', views.unban_user, name='unban_user'),


]
