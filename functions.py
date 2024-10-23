import sqlite3
from logging import getLogger

# создаем логер с таким же именем как у файла
logger = getLogger(__name__)


# подключаемся к бд
with sqlite3.connect('recipes1.sqlite', check_same_thread=False) as connection:
    cursor = connection.cursor()
logger.info("Подключение к базе данных")


# метод кладет данные из бд в список
def select_data():
    cursor.execute("SELECT * FROM recipes1")
    recipes_list = cursor.fetchall()
    logger.debug("Получены данные из базы данных")
    return recipes_list


# метод добавляет рецепт юзера в бд
def add_user_recipe(user_data):
    query = " INSERT INTO recipes1 (description, url, ingredients, autor) VALUES(?,?,?,?); "
    cursor.execute(query, user_data)
    connection.commit()
    logger.debug("Добавлены новые данные в БД")


# метод обновляет название рецепта
def update_recipe_name(old_name, new_name):
    query = " UPDATE recipes1 SET description = ? WHERE description = ? "
    cursor.execute(query, (new_name, old_name))
    connection.commit()
    logger.debug("Обновлено название рецепта")


# метод меняет ссылку на рецепт
def update_recipe_url(new_url, recipe_name):
    query = " UPDATE recipes1 SET url = ? WHERE description = ? "
    cursor.execute(query, (new_url, recipe_name))
    connection.commit()
    logger.debug("Обновлена ссылка рецепта")


# метод меняет основной ингредиент в рецепте
def update_ingredient(new_ingredient, recipe_name):
    query = " UPDATE recipes1 SET ingredients = ? WHERE description = ? "
    cursor.execute(query, (new_ingredient, recipe_name))
    connection.commit()
    logger.debug("Обновлен ингредиент рецепта")


# метод удаляет рецепт юзера из бд
def del_user_recipe(recipe_name):
    query = "DELETE FROM recipes1 WHERE description = ?"
    cursor.execute(query, (recipe_name,))
    connection.commit()
    logger.debug("Удален рецепт из базы данных")
