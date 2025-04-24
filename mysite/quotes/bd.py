import psycopg2
import json
import datetime

# Параметры подключения
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="root",
    host="127.0.0.1",
    port="5432"
)

cursor = conn.cursor()

# Получаем все данные из таблицы
cursor.execute("SELECT * FROM quotes_professors")

# Получаем результат
rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]

# Преобразуем результат в JSON-сериализуемый формат
def convert_value(value):
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.isoformat()
    return value

data = [ {col: convert_value(val) for col, val in zip(columns, row)} for row in rows ]

# Сохраняем в JSON файл
with open("data_bd/raw_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

# Закрываем соединение
cursor.close()
conn.close()
