import telebot
from telebot import types

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env
import os

# pip install pyTelegramBotAPI
# pip install python-dotenv

bot = telebot.TeleBot(os.getenv("TOKEN"))

big = "Все з великої"
big_sm = big.lower()
big_bg = big.upper()

small = "Все з маленької"
small_sm = small.lower()
small_bg = small.upper()

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton(small)
    markup.add(btn1)
    btn2 = types.KeyboardButton(big)
    markup.add(btn2)
    bot.send_message(message.chat.id, f"Привіт, <b>{message.from_user.first_name}</b>\n \
1) вибери кнопку <b>'Все з великої'</b>, якщо хочеш, щоб <b>усі літери</b> твого тексту відправлялися <b>з великої</b> або\
 вибери кнопку <b>'Все з маленької'</b>, якщо хочеш, щоб <b>усі літери</b> твого тексту відправлялися  <b>з маленької</b> \n \
2) <b>Відправив текст, який треба змінити</b>", parse_mode="html", reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

userCase = ""

def on_click(message, content_types=['text']):
    if message.text == small or message.text == big:
        global userCase
        userCase = message.text
        message = bot.send_message(message.chat.id, "Введіть текст, який треба змінити")
    if userCase == small:
        bot.register_next_step_handler(message, reply_to_user)
    elif userCase == big:
        bot.register_next_step_handler(message, reply_to_user)
    bot.register_next_step_handler(message, on_click)


def reply_to_user(message, content_types=['text']):
    if message.text is None:
        bot.send_message(message.chat.id, "Ви відправили не текстове повідомлення")
    elif message.text == "/start":
        start(message)
    elif message.text != big and message.text != big_bg and message.text != big_sm and message.text != small and message.text != small_bg and message.text != small_sm:
         if userCase == small:
            bot.send_message(message.chat.id, message.text.lower())
         if userCase == big:
            bot.send_message(message.chat.id, message.text.upper())



bot.polling(none_stop=True)