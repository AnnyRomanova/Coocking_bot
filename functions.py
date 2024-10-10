import sqlite3

# подключаемся к бд
with sqlite3.connect('recipes1.sqlite', check_same_thread=False) as connection:
    cursor = connection.cursor()


# метод кладет данные из бд в список
def select_data():
    cursor.execute("SELECT * FROM recipes1")
    recipes_list = cursor.fetchall()
    return recipes_list


# метод добавляет рецепт юзера в бд
def add_user_recipe(user_data):
    query = """ INSERT INTO recipes1 (description, url, ingredients, autor) VALUES(?,?,?,?); """
    cursor.execute(query, user_data)
    connection.commit()


# метод удаляет рецепт юзера из бд
def del_user_recipe(recipe_name):
    query = "DELETE FROM recipes1 WHERE description = ?"
    cursor.execute(query, (recipe_name,))
    connection.commit()
