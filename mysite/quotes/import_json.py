import json
from models import Faculties, Professors

# Откройте и прочитайте JSON-файл
with open('professors.json', 'r') as file:
    data = json.load(file)

# Запишем данные в таблицу Faculties
for entry in data:
    Faculties.objects.create(
        name=entry['name']
    )

print("Данные успешно загружены!")