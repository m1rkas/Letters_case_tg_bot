import telebot
from telebot import types

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env
import os

import constants


# pip install pyTelegramBotAPI
# pip install python-dotenv
# pip install telebot

bot = telebot.TeleBot(os.getenv("TOKEN"))

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton(constants.lang_ukr)
    btn2 = types.KeyboardButton(constants.lang_eng)
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, f"Choose language \nВиберіть мову", parse_mode="html", reply_markup=markup)
    bot.register_next_step_handler(message, greeting)

userLang = None
not_output = []
userCase = None
def greeting(message):
    global userLang
    if message.text is None:
        bot.send_message(message.chat.id, "Ви відправили не текстове повідомлення. Виберіть будь ласка мову користування ботом \n \
        You sent not a text message. Please select the language of the bot")
    elif constants.lang_ukr == message.text or constants.lang_eng == message.text:
        userLang = message.text
        markup = types.ReplyKeyboardMarkup()
        btn3 = types.KeyboardButton(constants.language[userLang]["small"])
        markup.add(btn3)
        btn4 = types.KeyboardButton(constants.language[userLang]["big"])
        markup.add(btn4)
        if userLang == constants.lang_ukr:
            bot.send_message(message.chat.id, f"Привіт, <b>{message.from_user.first_name}</b>\n \
            1) вибери кнопку <b>'Все з великої'</b>, якщо хочеш, щоб <b>усі літери</b> твого тексту відправлялися <b>з великої</b> або\
            вибери кнопку <b>'Все з маленької'</b>, якщо хочеш, щоб <b>усі літери</b> твого тексту відправлялися  <b>з маленької</b> \n \
            2) <b>Відправ текст, який треба змінити</b>", parse_mode="html", reply_markup=markup)
        if userLang == constants.lang_eng:
            bot.send_message(message.chat.id, f"Hello <b>{message.from_user.first_name}</b>\n \
            1) select the <b>'Everythong big'</b> button if you want <b>all letters</b> of your text to be sent with a <b>capital letter</b> or \n \
            select the <b>'Everything small'</b> button if you want <b>all letters</b> of your text to be sent with a <b>small letter</b> \n \
            2) Send the text you want to change", parse_mode="html", reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def on_click(message, content_types=['text']):
    global userCase
    global not_output
    not_output.append(constants.language[userLang]["big"])
    not_output.append(constants.language[userLang]["small"])
    not_output.append(constants.lang_ukr)
    not_output.append(constants.lang_eng)
    if message.text is None:
        bot.send_message(message.chat.id, constants.language[userLang]["non_text_message"])
    elif message.text == "/start":
        start(message)
    elif message.text == constants.language[userLang]["small"] or message.text == constants.language[userLang]["big"]:
        userCase = message.text
        message = bot.send_message(message.chat.id, constants.language[userLang]["change_text"])
        bot.register_next_step_handler(message, reply_to_user)
    bot.register_next_step_handler(message, on_click)


def reply_to_user(message, content_types=['text']):
    if message.text is None:
        bot.send_message(message.chat.id, constants.language[userLang]["non_text_message"])
        bot.register_next_step_handler(message, reply_to_user)
    elif message.text == "/start":
        start(message)
    elif message.text not in not_output:
         if userCase == constants.language[userLang]["small"]:
            bot.send_message(message.chat.id, message.text.lower())
         elif userCase == constants.language[userLang]["big"]:
            bot.send_message(message.chat.id, message.text.upper())
         bot.register_next_step_handler(message, reply_to_user)


# elif message.text != constans.language[userLang]["big"] and message.text != constans.language[userLang]["big_bg"] and message.text != constans.language[userLang]["big_sm"] and message.text != constans.language[userLang]["small"] and message.text != constans.language[userLang]["small_bg"] and message.text != constans.language[userLang]["small_sm"] and message.text != userLang:


bot.polling(none_stop=True)