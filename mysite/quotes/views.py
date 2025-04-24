from django.http import HttpResponse
import json
from .models import Faculties, Professors, Quotes, QuotesProfessors

def index(request):
    # with open('raw_data.json', 'r') as file:
    #     data = json.load(file)
    #
    # # Запишем данные в таблицу Faculties
    # for entry in data:
    #     QuotesProfessors.objects.create(
    #         quote_text=entry['quote_text'],
    #         professor=entry['professor'],
    #         faculty=entry['faculty'],
    #         faculty_0=entry['faculty_id'],
    #
    #     )
    #
    # print("Данные успешно загружены!")
    return HttpResponse("Дима лох")