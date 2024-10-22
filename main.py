import telebot  # импортируем библиотеку, с помощью которой пишем бота
from telebot import types  # модуль для кнопок со ссылками
import sqlite3  # для работы с базой данных
import functions  # для выполнения SQL-запросов
from logging import getLogger, basicConfig, DEBUG, FileHandler  # для логирования

# настраиваем логирование
logger = getLogger() # создание своего логера
file_handler = FileHandler("logs.log", encoding="utf-8")  # создаем файл, куда будут сохраняться логи
file_handler.setLevel(DEBUG)  # устанавливаем уровень логов, которые будут сохраняться в файл
FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # формат вывода время:название файла:уровень:сообщение
basicConfig(level=DEBUG, format=FORMAT, handlers=[file_handler])  # устанавливаем самый низкий уровень логирования, куда и в каком виде сохраняем логи

# подключаемся к бд
with sqlite3.connect('recipes1.sqlite', check_same_thread=False) as connection:
    cursor = connection.cursor()

bot = telebot.TeleBot(
    "")  # привязываем бота в телеге через ключ, который выдал BotFather


# Декоратор, где прописываем функции для команд юзера через /
@bot.message_handler(commands=["start"])  # можно прописать несколько команд через запятую
def start(message):
    bot.send_message(message.chat.id, "Привет! Просто напиши ингредиент, "
                                      "который хочешь видеть в своем блюде, а я подскажу, "
                                      "что вкусного с ним можно приготовить."
                                      "Можешь написать несколько ингредиентов через пробел")
    logger.info("Запущена команда start")
    bot.register_next_step_handler(message, list_of_recipes)


# Юзер отправляет ингредиент, в ответ список рецептов на кнопках
def list_of_recipes(message):
    ingredients = message.text.lower().split()  # текст, который отправляет юзер (ингредиент)
    logger.debug("Ингредиенты пользователя: %s", ingredients)

    markup = types.InlineKeyboardMarkup()
    for recipe in functions.select_data():
        for ingredient in ingredients:
            if ingredient in recipe[3]:
                markup.add(types.InlineKeyboardButton(recipe[1], url=recipe[2]))

    bot.send_message(message.chat.id, "Выбери рецепт", reply_markup=markup)
    logger.info("Команда start выполнена")


# возможность юзера добавить рецепт в бд
user_recipe = []


@bot.message_handler(commands=["add_recipe"])
def start_adding_recipe(message):
    logger.info("Запущена команда add_recipe")
    bot.send_message(message.chat.id, "Введи название рецепта")
    bot.register_next_step_handler(message, add_recipe_name)


def add_recipe_name(message):
    recipe_name = message.text
    logger.debug("Название рецепта: %s", recipe_name)
    user_recipe.append(recipe_name)
    bot.send_message(message.chat.id, "Теперь отправь ссылку на рецепт")
    bot.register_next_step_handler(message, add_link)


def add_link(message):
    link = message.text
    logger.debug("Ссылка рецепта: %s", link)
    user_recipe.append(link)
    bot.send_message(message.chat.id, "Отлично! Осталось написать основной ингредиент, из которого состоит это блюдо")
    bot.register_next_step_handler(message, add_ingredient)


def add_ingredient(message):
    ingredient = message.text
    logger.debug("Ингредиент рецепта: %s", ingredient)
    bot.send_message(message.chat.id, "Супер! Твой рецепт добавлен")
    user_recipe.append(ingredient)
    user_recipe.append(message.from_user.id)
    user_data = tuple(user_recipe)
    functions.add_user_recipe(user_data)
    user_recipe.clear()
    logger.info("Команда add_recipe выполнена")


# изменение названия рецепта юзера
@bot.message_handler(commands=["change_recipe_name"])
def start_change_recipe_name(message):
    logger.info("Команда change_recipe_name запущена")
    bot.send_message(message.chat.id, "Какой рецепт ты хочешь изменить? Введи старое название")
    bot.register_next_step_handler(message, check_name)


def check_name(message):
    old_recipe_name = message.text
    logger.debug("Название рецепта для изменения: %s", old_recipe_name)
    recipes_list = functions.select_data()
    user_id = message.from_user.id
    flag = False
    for recipe in recipes_list:
        if old_recipe_name in recipe and user_id in recipe:
            logger.debug("Проверка на соответствие id пользователя пройдена")
            flag = True
    if flag is True:
        bot.send_message(message.chat.id, "Хорошо, а теперь напиши новое название для этого рецепта")
        bot.register_next_step_handler(message, change_recipe_name, old_recipe_name)
    else:
        logger.debug("Проверка на соответствие id пользователя не пройдена")
        bot.send_message(message.chat.id, "Этот рецепт изменить нельзя")


def change_recipe_name(message, old_recipe_name):
    new_recipe_name = message.text
    logger.debug("Новое название рецепта: %s", new_recipe_name)
    functions.update_recipe_name(old_recipe_name, new_recipe_name)
    bot.send_message(message.chat.id, "Название изменено")
    logger.info("Команда change_recipe_name выполнена")


# возможность юзера изменить ссылку на свой рецепт
@bot.message_handler(commands=["change_recipe_url"])
def start_change_recipe_url(message):
    logger.info("Команда change_recipe_url запущена")
    bot.send_message(message.chat.id, "В каком рецепте изменить ссылку? Введи название рецепта")
    bot.register_next_step_handler(message, check_name_url)


def check_name_url(message):
    recipe_name = message.text
    logger.debug("Название рецепта для изменения: %s", recipe_name)
    recipes_list = functions.select_data()
    user_id = message.from_user.id
    flag = False
    for recipe in recipes_list:
        if recipe_name in recipe and user_id in recipe:
            logger.debug("Проверка на соответствие id пользователя пройдена")
            flag = True
    if flag is True:
        bot.send_message(message.chat.id, "Ок, пришли новую ссылку")
        bot.register_next_step_handler(message, change_recipe_url, recipe_name)
    else:
        logger.debug("Проверка на соответствие id пользователя не пройдена")
        bot.send_message(message.chat.id, "Этот рецепт изменить нельзя")


def change_recipe_url(message, recipe_name):
    new_recipe_url = message.text
    logger.debug("Новая ссылка рецепта: %s", new_recipe_url)
    functions.update_recipe_url(new_recipe_url, recipe_name)
    bot.send_message(message.chat.id, "Ссылка изменена")
    logger.info("Команда change_recipe_url выполнена")


# возможность юзера изменить ингредиент в своем рецепте
@bot.message_handler(commands=["change_ingredient"])
def start_change_ingredient(message):
    logger.info("Команда change_ingredient запущена")
    bot.send_message(message.chat.id, "В каком рецепте изменить ингредиент? Введи название рецепта")
    bot.register_next_step_handler(message, check_name_ingredient)


def check_name_ingredient(message):
    recipe_name = message.text
    logger.debug("Название рецепта для изменения: %s", recipe_name)
    recipes_list = functions.select_data()
    user_id = message.from_user.id
    flag = False
    for recipe in recipes_list:
        if recipe_name in recipe and user_id in recipe:
            logger.debug("Проверка на соответствие id пользователя пройдена")
            flag = True
    if flag is True:
        bot.send_message(message.chat.id, "Ок, пришли новый ингредиент")
        bot.register_next_step_handler(message, change_recipe_ingredient, recipe_name)
    else:
        logger.debug("Проверка на соответствие id пользователя не пройдена")
        bot.send_message(message.chat.id, "Этот рецепт изменить нельзя")


def change_recipe_ingredient(message, recipe_name):
    new_recipe_ingredient = message.text
    logger.debug("Новый ингредиент рецепта: %s", new_recipe_ingredient)
    functions.update_ingredient(new_recipe_ingredient, recipe_name)
    bot.send_message(message.chat.id, "Ингредиент изменен")
    logger.info("Команда change_ingredient выполнена")


# возможность юзера удалить свой рецепт из бд
@bot.message_handler(commands=["delete_recipe"])
def start_del_recipe(message):
    logger.info("Команда delete_recipe запущена")
    bot.send_message(message.chat.id, "Какой рецепт ты хочешь удалить? Введи название")
    bot.register_next_step_handler(message, del_recipe)


def del_recipe(message):
    recipe_name = message.text
    logger.debug("Название рецепта для удаления: %s", recipe_name)
    recipes_list = functions.select_data()
    user_id = message.from_user.id
    flag = False
    for recipe in recipes_list:
        if recipe_name in recipe and user_id in recipe:
            flag = True
        else:
            flag = False
    if flag is False:
        logger.debug("Проверка на соответствие id пользователя не пройдена")
        bot.send_message(message.chat.id, "Я не могу удалить этот рецепт :(")
    else:
        logger.debug("Проверка на соответствие id пользователя пройдена")
        functions.del_user_recipe(recipe_name)
        bot.send_message(message.chat.id, "Твой рецепт удален")
        logger.info("Команда delete_recipe выполнена")


bot.polling(non_stop=True)