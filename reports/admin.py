from django.contrib import admin

from .models import Report, EvaluateOrganizer, Scholarship

admin.site.register(Report)
admin.site.register(EvaluateOrganizer)
admin.site.register(Scholarship)
