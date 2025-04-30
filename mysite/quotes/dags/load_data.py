from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.models import Variable
from vk_api import VkApi, VkTools
from vk_api.exceptions import ApiError
from airflow.providers.postgres.hooks.postgres import PostgresHook
import re
from faculties import faculties
# Импортируем список
token = Variable.get('vk_api_token')
group_id = '129370820'


def parse_data(post: dict) -> tuple:
    result = {
        'quote': None,
        'author': None,
        'faculty': None,
        'date': None,
        'likes': None,
        'reposts': None
    }

    try:
        text = post['text']
        # if ((text.count('»') + text.count('«')) >
        pattern = r"[А-ЯЁ]\.\s?[А-ЯЁ]\.\s?[А-ЯЁ][а-яё]+"
        matches = re.search(pattern, text)
        result['author'] = matches[0]
        result['quote'] = text.split(matches[0])[0].strip('\n')
        result['faculty'] = post['text'].split('#')[2].strip()
        result['date'] = datetime.fromtimestamp(post['date'])
        result['likes'] = post['likes']
        result['reposts'] = post['reposts']

    except Exception as e:
        print(post)
        print(f"Ошибка при парсинге поста: {e}")

    return tuple(result.values())


def extract_load_raw_data():

    vk_session = VkApi(token=token)

    tools = VkTools(vk_session)
    try:
        wall_posts = tools.get_all('wall.get', max_count=100, values={
            'owner_id': f"-{group_id}"})
        posts_data = []
        for post in wall_posts['items']:
            if 'quotes' in post['text'] and 'цитаты' in post['text'] and 'copy_history' not in post:
                post_data = {'id': post['id'], 'text': post['text'], 'date': post['date'], 'likes': post['likes']['count'],
                             'reposts': post['reposts']['count']}
                # post_data['comments'] = vk.wall.getComments(owner_id= f"-{group_id}", post_id = post_data['id'], count=5)['items'][0]['text']
                posts_data.append(parse_data(post_data))

    except ApiError as e:
        print(f"Ошибка VK API: {e}")

    hook = PostgresHook(postgres_conn_id='postgres_conn')
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE raw_data RESTART IDENTITY CASCADE;")
    cursor.execute("TRUNCATE TABLE quotes RESTART IDENTITY CASCADE;")
    cursor.execute("TRUNCATE TABLE faculties RESTART IDENTITY CASCADE;")
    cursor.execute("TRUNCATE TABLE professors RESTART IDENTITY CASCADE;")
    conn.commit()
    cursor.executemany(
        "INSERT INTO raw_data (quote_text, professor, faculty, date, likes, reposts) VALUES (%s, %s, %s, %s, %s, %s)",
        posts_data
    )

    query = "DELETE FROM raw_data WHERE faculty NOT IN %s;"
    cursor.execute(query, (tuple(faculties),))
    conn.commit()
    cursor.close()
    conn.close()


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Определение DAG
with DAG(
    'extract_load_data',                      # Идентификатор DAG
    default_args=default_args,
    description='Извлекаем данные из vk_api, загружаем в postgresql',
    schedule_interval=timedelta(days=7),  # Запускать ежедневно
    start_date=datetime(2025, 1, 1),    # Дата начала выполнения
    catchup=False,                      # Не выполнять пропущенные запуски
) as dag:

    # Определение задачи
    extract_load = PythonOperator(
        task_id='extract_load_data',          # Идентификатор задачи
        python_callable=extract_load_raw_data,    # Функция для выполнения
    )
    update_faculties = PostgresOperator(
        task_id='update_faculties',
        postgres_conn_id='postgres_conn',
        sql="sql/faculties.sql")

    update_professors = PostgresOperator(
        task_id='update_professors',
        postgres_conn_id='postgres_conn',
        sql="sql/professors.sql")


    update_quotes = PostgresOperator(
        task_id='update_quotes',
        postgres_conn_id='postgres_conn',
        sql="sql/quotes.sql")
    extract_load >> update_faculties >> update_professors >> update_quotes