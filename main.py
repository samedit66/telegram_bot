import datetime

import telebot
from telebot import types

import config
import contact_book


contact_builder = contact_book.SqlContactBuilder()
bot = telebot.TeleBot(config.token)


def create_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    add_contact_btn = types.KeyboardButton("Добавить контакт")
    show_contacts_btn = types.KeyboardButton("Показать все контакты")
    keyboard.add(add_contact_btn, show_contacts_btn)

    return keyboard


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id,
                     "Привет! Я - бот для контактов.",
                     reply_markup=create_main_keyboard())
    bot.register_next_step_handler(message, handle_main_commands)


def handle_main_commands(message):

    if message.text == "Добавить контакт":
        delete_keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Как зовут контакта?", reply_markup=delete_keyboard)
        bot.register_next_step_handler(message, process_name_step)
    elif message.text == "Показать все контакты":
        contacts = contact_builder.get_contacts(message.chat.id)
        if len(contacts) > 0:
            bot.send_message(message.chat.id, "Список всех контактов:")

            for number, contact in enumerate(contacts, start=1):
                output_message = f"{number}. {contact}"
                bot.send_message(message.chat.id, output_message)
        else:
            bot.send_message(message.chat.id, "Список контактов пуст")

        bot.register_next_step_handler(message, handle_main_commands)
    else:
        bot.send_message(message.chat.id, "Не понял...")
        bot.register_next_step_handler(message, handle_main_commands)


def process_name_step(message):
    name = message.text

    if not name:
        bot.send_message(message.chat.id, "Имя не может быть пустым!")
        bot.register_next_step_handler(message, process_name_step)
        return

    contact_builder.add_name(message.chat.id, name)
    
    bot.send_message(message.chat.id, "Номер телефона:")
    bot.register_next_step_handler(message, process_phone_number_step)


def process_phone_number_step(message):
    phone_number = message.text

    if not phone_number:
        bot.send_message(message.chat.id, "Номер телефона не может быть пустым!")
        bot.register_next_step_handler(message, process_phone_number_step)
        return
    
    contact_builder.add_phone_number(message.chat.id, phone_number)

    bot.send_message(message.chat.id, "Описание:")
    bot.register_next_step_handler(message, process_description_step)


def process_description_step(message):
    description = message.text

    contact_builder.add_description(message.chat.id, description)
    contact_builder.build(message.chat.id)

    bot.send_message(message.chat.id,
                     "Контакт создан!",
                     reply_markup=create_main_keyboard())
    bot.register_next_step_handler(message, handle_main_commands)


bot.infinity_polling()
