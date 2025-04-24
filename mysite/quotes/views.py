from django.http import HttpResponse
import json
from .models import Faculties, Professors, Quotes, QuotesProfessors
import os
def index(request):
    with open('quotes/quotes.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Запишем данные в таблицу Faculties
    for entry in data:
        for entry in data:
            try:
                professor = Professors.objects.get(pk=entry['professor_id'])
            except Professors.DoesNotExist:
                print(f"Пропущена цитата с professor_id={entry['professor_id']} — такого профессора нет.")
                continue
        Quotes.objects.create(
            text=entry['text'],
            professor=professor,
            likes_count=entry['likes_count'],
            reposts_count=entry['reposts_count'],
            date=entry['date']
        )

    # print("Данные успешно загружены!")
    return HttpResponse(f"Current working directory: {os.getcwd()}")