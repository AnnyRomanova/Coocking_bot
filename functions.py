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
    query = " INSERT INTO recipes1 (description, url, ingredients, autor) VALUES(?,?,?,?); "
    cursor.execute(query, user_data)
    connection.commit()


# метод обновляет название рецепта
def update_recipe_name(old_name, new_name):
    query = " UPDATE recipes1 SET description = ? WHERE description = ? "
    cursor.execute(query, (new_name, old_name))
    connection.commit()


# метод меняет ссылку на рецепт
def update_recipe_url(new_url, recipe_name):
    query = " UPDATE recipes1 SET url = ? WHERE description = ? "
    cursor.execute(query, (new_url, recipe_name))
    connection.commit()


# метод меняет основной ингредиент в рецепте
def update_ingredient(new_ingredient, recipe_name):
    query = " UPDATE recipes1 SET ingredients = ? WHERE description = ? "
    cursor.execute(query, (new_ingredient, recipe_name))
    connection.commit()


# метод удаляет рецепт юзера из бд
def del_user_recipe(recipe_name):
    query = "DELETE FROM recipes1 WHERE description = ?"
    cursor.execute(query, (recipe_name,))
    connection.commit()
