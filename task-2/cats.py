from pymongo import MongoClient
from pymongo.errors import PyMongoError

import os
import dotenv

# Завантаження файлу .env
dotenv.load_dotenv()

# Підключення до MongoDB
client = MongoClient(f"mongodb+srv://{os.getenv('UNAME')}:{os.getenv('PASSWORD')}@mongo.waelic8.mongodb.net/?retryWrites=true&w=majority&appName=Mongo")
db = client.mds
collection = db['cats']

# Читання (Read)

def get_all_cats():
    """Повертає всіх котів у колекції"""
    try:
        return list(collection.find())
    except PyMongoError as e:
        print(f"Помилка при отриманні усіх котів: {e}")
        return []

def get_cat_by_name(name):
    """Повертає кота за ім'ям"""
    try:
        return collection.find_one({'name': name})
    except PyMongoError as e:
        print(f"Помилка при отриманні кота за ім'ям '{name}': {e}")
        return None

def print_cat_info():
    """Виводить інформацію про кота за ім'ям, яке введе користувач"""
    name = input("Введіть ім'я кота: ")
    cat = get_cat_by_name(name)
    if cat:
        print(f"\nІнформація про кота '{name}':")
        print(cat)
    else:
        print(f"Кота з ім'ям '{name}' не знайдено.")

def add_new_cat():
    """Додає нового кота"""
    name = input("Введіть ім'я нового кота: ")
    age = int(input("Введіть вік нового кота: "))
    features = input("Введіть характеристики нового кота (через кому): ").split(',')
    cat = {
        "name": name,
        "age": age,
        "features": features
    }
    try:
        collection.insert_one(cat)
        print(f"Кота '{name}' успішно додано до бази даних.")
    except PyMongoError as e:
        print(f"Помилка при додаванні кота: {e}")

# Оновлення (Update)

def update_cat_age_by_name(name):
    """Оновлює вік кота за ім'ям"""
    new_age = int(input("Введіть новий вік кота: "))
    try:
        collection.update_one({'name': name}, {'$set': {'age': new_age}})
        print(f"Вік кота '{name}' успішно оновлено.")
    except PyMongoError as e:
        print(f"Помилка при оновленні віку кота: {e}")

def add_feature_to_cat_by_name(name):
    """Додає нову характеристику коту за ім'ям"""
    new_feature = input("Введіть нову характеристику: ")
    try:
        collection.update_one({'name': name}, {'$push': {'features': new_feature}})
        print(f"Нову характеристику успішно додано до кота '{name}'.")
    except PyMongoError as e:
        print(f"Помилка при додаванні характеристики коту: {e}")

# Видалення (Delete)

def delete_cat_by_name(name):
    """Видаляє кота за ім'ям"""
    try:
        result = collection.delete_one({'name': name})
        if result.deleted_count > 0:
            print(f"Кота '{name}' успішно видалено з бази даних.")
        else:
            print(f"Кота з ім'ям '{name}' не знайдено.")
    except PyMongoError as e:
        print(f"Помилка при видаленні кота: {e}")

def delete_all_cats():
    """Видаляє всіх котів з колекції"""
    try:
        result = collection.delete_many({})
        print(f"Всі коти успішно видалено з бази даних. Кількість видалених записів: {result.deleted_count}")
    except PyMongoError as e:
        print(f"Помилка при видаленні котів: {e}")

# Основний цикл програми
while True:
    print("\nМеню:")
    print("1. Вивести всіх котів")
    print("2. Пошук кота за ім'ям")
    print("3. Додати нового кота")
    print("4. Оновити вік кота за ім'ям")
    print("5. Додати нову характеристику до списку features кота за ім'ям")
    print("6. Видалити кота за ім'ям")
    print("7. Видалити всіх котів")
    print("8. Вийти з програми")

    choice = input("Виберіть дію: ")

    if choice == "1":
        cats = get_all_cats()
        if cats:
            print("\nУсі коти:")
            for cat in cats:
                print(cat)
        else:
            print("Немає котів у базі даних.")
    elif choice == "2":
        print_cat_info()
    elif choice == "3":
        add_new_cat()
    elif choice == "4":
        name = input("Введіть ім'я кота, вік якого потрібно оновити: ")
        update_cat_age_by_name(name)
    elif choice == "5":
        name = input("Введіть ім'я кота, до якого потрібно додати нову характеристику: ")
        add_feature_to_cat_by_name(name)
    elif choice == "6":
        name = input("Введіть ім'я кота, якого потрібно видалити: ")
        delete_cat_by_name(name)
    elif choice == "7":
        delete_all_cats()
    elif choice == "8":
        print("До побачення!")
        break
    else:
        print("Невірний вибір. Будь ласка, виберіть дію зі списку.")
