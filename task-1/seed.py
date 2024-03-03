from random import randint

from faker import Faker
from psycopg2 import DatabaseError

from connect import create_connect


with create_connect() as conn:
    # Ініціалізація курсора
    cur = conn.cursor()

    # Ініціалізація об'єкту Faker
    fake = Faker()

    # Заповнення таблиці users
    for _ in range(10):  # заповнюємо 10 користувачів
        fullname = fake.name()
        email = fake.email()
        cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email))

    # Заповнення таблиці status
    statuses = ['new', 'in progress', 'completed']
    for status in statuses:
        cur.execute("INSERT INTO status (name) VALUES (%s)", (status,))

    # Заповнення таблиці tasks
    for _ in range(20):  # заповнюємо 20 завдань
        title = fake.sentence(nb_words=4)
        description = fake.text()
        status_id = randint(1, len(statuses))  # вибираємо випадковий статус
        user_id = randint(1, 10)  # вибираємо випадкового користувача
        cur.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
                    (title, description, status_id, user_id))

    # Збереження змін до бази даних
    conn.commit()
