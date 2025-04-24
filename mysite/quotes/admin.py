from django.contrib import admin
from .models import QuotesProfessors, Quotes, Faculties, Professors

# Регистрация моделей для админки
admin.site.register(Quotes)
admin.site.register(Faculties)
admin.site.register(Professors)
