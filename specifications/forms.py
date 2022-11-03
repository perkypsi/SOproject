from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django import forms
from django.core.exceptions import ValidationError

from .models import Document


class DocumentDownload(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document',
                  'name',
                  'description',
                  ]
        widgets = {
            'document': forms.FileInput(attrs={"class": "form-control"}),
            'name': forms.TextInput(attrs={"class": "form-control"}),
            'description': forms.Textarea(attrs={"class": "form-control light-so-l", "rows": "3"}),
        }
