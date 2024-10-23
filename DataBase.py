import sqlite3  # база данных
from parsing import egg_list, bread_list, sausage_list, sausage2_list, cheese_list
from logging import getLogger, basicConfig, DEBUG  # для логирования

# настраиваем логирование
logger = getLogger()  # создание своего логера
FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # формат вывода время-название файла-уровень-сообщение
basicConfig(level=DEBUG, format=FORMAT)  # устанавливаем самый низкий уровень логирования, куда и в каком виде сохраняем логи


# подключаемся к бд
with sqlite3.connect('recipes1.sqlite') as connection:
    cursor = connection.cursor()
logger.info("Подключение к базе данных")


# Создаем таблицу с 5 полями
def create_db():
    cursor.execute("""CREATE TABLE recipes1 (
        id int auto_increment primary key, 
        description text,
        url text,
        ingredients text,
        autor int
        )""")
    logger.info("База данных с полями создана")


# Добавляем данные в таблицу
def fill_the_table():
    # query_list = [
    #     ('Тост с авокадо, солёной сёмгой и яйцом пашот',
    #      'https://www.russianfood.com/recipes/recipe.php?rid=163688',
    #      'яйцо'),
    #     ('Омлет с грибами и шпинатом', 'https://www.russianfood.com/recipes/recipe.php?rid=168116', 'яйцо, шпинат'),
    #     ('Яичница с индейкой и помидорами', 'https://www.russianfood.com/recipes/recipe.php?rid=164679', 'яйцо, помидор'),
    #     ('Горячие бутерброды', 'https://www.russianfood.com/recipes/recipe.php?rid=170561', 'хлеб'),
    #     ('Французские тосты', 'https://www.russianfood.com/recipes/recipe.php?rid=126745', 'хлеб, яйцо'),
    #     ('Сендвич', 'https://www.russianfood.com/recipes/recipe.php?rid=116094', 'хлеб')
    # ]
    query = """ INSERT INTO recipes1 (description, url, ingredients, autor) VALUES(?,?,?,?); """

    cursor.executemany(query, egg_list)
    cursor.executemany(query, bread_list)
    cursor.executemany(query, sausage_list)
    cursor.executemany(query, sausage2_list)
    cursor.executemany(query, cheese_list)
    connection.commit()  # обновляем бд
    logger.info("Таблица в базе данных заполнена")


# Создаем бд
create_db()

# Заполняем БД
fill_the_table()