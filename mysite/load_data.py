# load_quotes.py
import json
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')  # замените на ваш проект
django.setup()

from mysite.quotes.models import Quotes, Professors

with open('quotes/quotes.json', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    professor_id = item.pop("professor_id", None)

    try:
        professor = Professors.objects.get(id=professor_id) if professor_id else None
        Quotes.objects.create(professor=professor, **item)
        print(f"✅ Добавлена цитата: {item['text'][:50]}...")
    except Professors.DoesNotExist:
        print(f"⚠️ Пропущено: профессор с id={professor_id} не найден")
