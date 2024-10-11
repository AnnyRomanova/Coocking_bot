import telebot  # импортируем библиотеку, с помощью которой пишем бота
from telebot import types  # модуль для кнопок с ссылками
import sqlite3  # для работы с базой данных
import functions  # для выполнения SQL-запросов

# подключаемся к бд
with sqlite3.connect('recipes1.sqlite', check_same_thread=False) as connection:
    cursor = connection.cursor()

bot = telebot.TeleBot(
    "7226047666:AAEqyEN6mz-FK2E8IOHR7wG2h1mOpDmsSsA")  # привязываем бота в телеге через ключ, который выдал BotFather


# Декоратор, где прописываем функции для команд юзера через /
@bot.message_handler(commands=["start"])  # можно прописать несколько команд через запятую
def start(message):
    bot.send_message(message.chat.id, "Привет! Просто напиши ингредиент, "
                                      "который хочешь видеть в своем блюде, а я подскажу, "
                                      "что вкусного с ним можно приготовить")


# возможность юзера добавить рецепт в бд
user_recipe = []


@bot.message_handler(commands=["add_recipe"])
def start_adding_recipe(message):
    bot.send_message(message.chat.id, "Введи название рецепта")
    bot.register_next_step_handler(message, add_recipe_name)


def add_recipe_name(message):
    recipe_name = message.text
    user_recipe.append(recipe_name)
    bot.send_message(message.chat.id, "Теперь отправь ссылку на рецепт")
    bot.register_next_step_handler(message, add_link)


def add_link(message):
    link = message.text
    user_recipe.append(link)
    bot.send_message(message.chat.id, "Отлично! Осталось написать основной ингредиент, из которого состоит это блюдо")
    bot.register_next_step_handler(message, add_ingredient)


def add_ingredient(message):
    ingredient = message.text
    bot.send_message(message.chat.id, "Супер! Твой рецепт добавлен")
    user_recipe.append(ingredient)
    user_recipe.append(message.from_user.id)
    user_data = tuple(user_recipe)
    functions.add_user_recipe(user_data)
    user_recipe.clear()


# изменение названия рецепта юзера
@bot.message_handler(commands=["change_recipe_name"])
def start_change_recipe_name(message):
    bot.send_message(message.chat.id, "Какой рецепт ты хочешь изменить? Введи старое название")
    bot.register_next_step_handler(message, check_name)


def check_name(message):
    old_recipe_name = message.text
    recipes_list = functions.select_data()
    user_id = message.from_user.id
    flag = False
    for recipe in recipes_list:
        if old_recipe_name in recipe and user_id in recipe:
            flag = True
    if flag is True:
        bot.send_message(message.chat.id, "Хорошо, а теперь напиши новое название для этого рецепта")
        bot.register_next_step_handler(message, change_recipe_name, old_recipe_name)
    else:
        bot.send_message(message.chat.id, "Этот рецепт изменить нельзя")


def change_recipe_name(message, old_recipe_name):
    new_recipe_name = message.text
    functions.update_recipe_name(old_recipe_name, new_recipe_name)
    bot.send_message(message.chat.id, "Название изменено")



# возможность юзера удалить свой рецепт из бд
@bot.message_handler(commands=["delete_recipe"])
def start_del_recipe(message):
    bot.send_message(message.chat.id, "Какой рецепт ты хочешь удалить? Введи название")
    bot.register_next_step_handler(message, del_recipe)


def del_recipe(message):
    recipe_name = message.text
    recipes_list = functions.select_data()
    user_id = message.from_user.id
    flag = False
    for recipe in recipes_list:
        if recipe_name in recipe and user_id in recipe:
            flag = True
        else:
            flag = False
    if flag is False:
        bot.send_message(message.chat.id, "Я не могу удалить этот рецепт :(")
    else:
        functions.del_user_recipe(recipe_name)
        bot.send_message(message.chat.id, "Твой рецепт удален")




# Юзер отправляет ингредиент, в ответ список рецептов на кнопках
@bot.message_handler()
def list_of_recipes(message):
    ingredient = message.text.lower()  # текст, который отправляет юзер (ингредиент)

    markup = types.InlineKeyboardMarkup()
    for recipe in functions.select_data():
        if ingredient in recipe[3]:
            markup.add(types.InlineKeyboardButton(recipe[1], url=recipe[2]))

    bot.send_message(message.chat.id, "Выбери рецепт", reply_markup=markup)


bot.polling(non_stop=True)
