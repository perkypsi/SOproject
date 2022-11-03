import datetime

from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django import forms
from django.core.exceptions import ValidationError

from .models import Profile, Event


class ProfileCreationForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ['username',
                  'first_name',
                  'last_name',
                  'patronymic',
                  'direct',
                  'post',
                  'access_level',
                  'birthdate',
                  'edu_group',
                  'phone_number',
                  'link_social',
                  'email',
                  ]
        widgets = {
            'username': forms.TextInput(attrs={"class": "form-control"}),
            'first_name': forms.TextInput(attrs={"class": "form-control"}),
            'last_name': forms.TextInput(attrs={"class": "form-control"}),
            'patronymic': forms.TextInput(attrs={"class": "form-control"}),
            'direct': forms.Select(attrs={"class": "form-control"}),
            'post': forms.TextInput(attrs={"class": "form-control"}),
            'access_level': forms.Select(attrs={"class": "form-control"}),
            'birthdate': forms.DateInput(format=('%Y-%m-%d'),
                                         attrs={'class': 'form-control', 'placeholder': 'Select Date', 'type': 'date'}),
            'edu_group': forms.TextInput(attrs={"class": "form-control"}),
            'phone_number': forms.TextInput(attrs={"class": "form-control"}),
            'link_social': forms.TextInput(attrs={"class": "form-control"}),
            'email': forms.TextInput(attrs={"class": "form-control"}),
        }


class ProfileChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = Profile
        fields = ['username',
                  'first_name',
                  'last_name',
                  'patronymic',
                  'direct',
                  'post',
                  'access_level',
                  'birthdate',
                  'edu_group',
                  'phone_number',
                  'link_social',
                  'email',
                  ]
        widgets = {
            'username': forms.TextInput(attrs={"class": "form-control"}),
            'first_name': forms.TextInput(attrs={"class": "form-control"}),
            'last_name': forms.TextInput(attrs={"class": "form-control"}),
            'patronymic': forms.TextInput(attrs={"class": "form-control"}),
            'direct': forms.Select(attrs={"class": "form-control"}),
            'post': forms.TextInput(attrs={"class": "form-control"}),
            'access_level': forms.Select(attrs={"class": "form-control"}),
            'birthdate': forms.DateInput(format=('%Y-%m-%d'),
                                         attrs={'class': 'form-control', 'placeholder': 'Select Date', 'type': 'date'}),
            'edu_group': forms.TextInput(attrs={"class": "form-control"}),
            'phone_number': forms.TextInput(attrs={"class": "form-control"}),
            'link_social': forms.TextInput(attrs={"class": "form-control"}),
            'email': forms.TextInput(attrs={"class": "form-control"}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True, label="Логин",
                               widget=forms.TextInput(attrs={"class": "form-control rounded"}))
    password = forms.CharField(max_length=100, required=True, label="Пароль",
                               widget=forms.PasswordInput(attrs={"class": "form-control rounded"}))

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        return password


class CreateEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name_event',
                  'direct_event',
                  'aims_event',
                  'concept_event',
                  'amount_participants',
                  'place_event',
                  'need_info',
                  'need_external',
                  'date_event',
                  ]
        widgets = {
            'name_event': forms.TextInput(attrs={"class": "form-control light-so-l"}),
            'direct_event': forms.Select(attrs={"class": "form-control light-so-l"}),
            'aims_event': forms.Textarea(attrs={"class": "form-control light-so-l", "rows": "3"}),
            'concept_event': forms.Textarea(attrs={"class": "form-control light-so-l", "rows": "3"}),
            'amount_participants': forms.TextInput(attrs={"class": "form-control light-so-l", "type": "number", "min": "1"}),
            'place_event': forms.Textarea(attrs={"class": "form-control light-so-l", "rows": "3"}),
            'need_info': forms.CheckboxInput(attrs={"class": "form-check-input light-so-l", "role": "switch"}),
            'need_external': forms.CheckboxInput(attrs={"class": "form-check-input light-so-l", "role": "switch"}),
            'date_event': forms.DateInput(format=('%Y-%m-%d'),
                                          attrs={'class': 'form-control light-so-l', 'placeholder': 'Select Date',
                                                 'type': 'date'}),
        }

    def clean_date_event(self):
        date = self.cleaned_data['date_event']
        if date <= datetime.date.today() \
                and self.cleaned_data['need_info'] \
                and self.cleaned_data['need_external']:
            raise ValidationError("Дата введена некорректно!")
        return date


class EditEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name_event', 'direct_event', 'aims_event',
                  'concept_event', 'amount_participants', 'place_event',
                  'date_event', 'step_one', 'step_two', 'step_three', 'step_four',
                  'step_five', 'document_for_info', 'document_for_external',
                  'additional_document']
        widgets = {
            'name_event': forms.TextInput(attrs={"class": "form-control"}),
            'direct_event': forms.Select(attrs={"class": "form-control"}),
            'aims_event': forms.Textarea(attrs={"class": "form-control", "rows": "3"}),
            'concept_event': forms.Textarea(attrs={"class": "form-control", "rows": "3"}),
            'amount_participants': forms.TextInput(attrs={"class": "form-control", "type": "number", "min": "1"}),
            'place_event': forms.Textarea(attrs={"class": "form-control", "rows": "3"}),
            'date_event': forms.DateInput(format=('%Y-%m-%d'),
                                          attrs={'class': 'form-control', 'placeholder': 'Select Date',
                                                 'type': 'date'}),
            'step_one': forms.Textarea(attrs={"class": "form-control", "rows": "3"}),
            'step_two': forms.Textarea(attrs={"class": "form-control", "rows": "3"}),
            'step_three': forms.Textarea(attrs={"class": "form-control", "rows": "3"}),
            'step_four': forms.Textarea(attrs={"class": "form-control", "rows": "3"}),
            'step_five': forms.Textarea(attrs={"class": "form-control", "rows": "3"}),

            'document_for_info': forms.TextInput(attrs={"class": "form-control"}),
            'document_for_external': forms.TextInput(attrs={"class": "form-control"}),
            'additional_document': forms.TextInput(attrs={"class": "form-control"})

        }

    def clean_date_event(self):
        date = self.cleaned_data['date_event']
        if date is None:
            raise ValidationError("Введите дату мероприятия")
        elif date <= datetime.date.today() \
                and self.cleaned_data['need_info'] \
                and self.cleaned_data['need_external']:
            raise ValidationError("Дата введена некорректно!")
        return date


class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget = forms.PasswordInput(attrs={"class": "form-control"})
        self.fields["new_password1"].widget = forms.PasswordInput(attrs={"class": "form-control"})
        self.fields["new_password2"].widget = forms.PasswordInput(attrs={"class": "form-control"})

