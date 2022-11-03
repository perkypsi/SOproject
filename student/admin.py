from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import ProfileCreationForm, ProfileChangeForm
from .models import Profile, StatusEvent, AccessLevel, Event, Notification, Direct, Ban


class ProfileAdmin(UserAdmin):
    add_form = ProfileCreationForm
    form = ProfileChangeForm
    model = Profile
    list_display = ['email', 'username', 'patronymic', 'rating', 'rating_score']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Event)
admin.site.register(Direct)
admin.site.register(AccessLevel)
admin.site.register(StatusEvent)
admin.site.register(Notification)
admin.site.register(Ban)