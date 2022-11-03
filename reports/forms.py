from django import forms
from django.core.exceptions import ValidationError

from .models import Report


class CreateReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['date_start',
                  'date_end',
                  'real_amount_participants',
                  'problems',
                  'need_info',
                  'need_external',
                  ]
        widgets = {
            'date_start': forms.DateInput(format=('%Y-%m-%d'),
                                          attrs={'class': 'form-control light-so-l', 'placeholder': 'Select Date',
                                                 'type': 'date'}),
            'date_end': forms.DateInput(format=('%Y-%m-%d'),
                                          attrs={'class': 'form-control light-so-l', 'placeholder': 'Select Date',
                                                 'type': 'date'}),
            'real_amount_participants': forms.TextInput(
                attrs={"class": "form-control light-so-l", "type": "number", "min": "1"}),
            'problems': forms.Textarea(attrs={"class": "form-control light-so-l", "rows": "3"}),
            'need_info': forms.CheckboxInput(attrs={"class": "form-check-input light-so-l", "role": "switch"}),
            'need_external': forms.CheckboxInput(attrs={"class": "form-check-input light-so-l", "role": "switch"}),

        }

    def clean_date_end(self):
        date_start = self.cleaned_data['date_start']
        date_end = self.cleaned_data['date_end']
        if date_end < date_start:
            raise ValidationError("Дата введена некорректно!")
        return date_end