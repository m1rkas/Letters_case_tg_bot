import telebot
from telebot import types

TOKEN = None

with open("token.txt") as f:
    TOKEN = f.read().strip()

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton("Все з маленької")
    markup.add(btn1)
    btn2 = types.KeyboardButton("Все з великої")
    markup.add(btn2)
    bot.send_message(message.chat.id, f"Привіт, <b>{message.from_user.first_name}</b>\n \
1) вибери кнопку <b>'Все з великої'</b>, якщо хочеш, щоб <b>усі літери</b> твого тексту відправлялися <b>з великої</b> або\
 вибери кнопку <b>'Все з маленької'</b>, якщо хочеш, щоб <b>усі літери</b> твого тексту відправлялися  <b>з маленької</b> \n \
2) <b>Відправив текст, який треба змінити</b>", parse_mode="html", reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

userCase = ""

def on_click(message, content_types=['text']):
    if message.text == "Все з маленької" or message.text == "Все з великої":
        global userCase
        if message.text == "Все з маленької":
            userCase = "Все з маленької"
        elif message.text == "Все з великої":
            userCase = "Все з великої"
        message = bot.send_message(message.chat.id, "Введіть текст, який треба змінити")
    if userCase == "Все з маленької":
        bot.register_next_step_handler(message, reply_to_user_low)
    elif userCase == "Все з великої":
        bot.register_next_step_handler(message, reply_to_user_up)
    bot.register_next_step_handler(message, on_click)


def reply_to_user_low(message, content_types=['text']):
    if message.text is None:
        bot.send_message(message.chat.id, "Ви відправили не текстове повідомлення")
    elif message.text == "/start":
        start(message)
    else:
        if message.text != "Все з великої" and message.text != "ВСЕ З ВЕЛИКОЇ" and message.text != "Все з маленької" and message.text != "ВСЕ З МАЛЕНЬКОЇ":
            bot.send_message(message.chat.id, message.text.lower())


def reply_to_user_up(message, content_types=['text']):
    if message.text is None:
        bot.send_message(message.chat.id, "Ви відправили не текстове повідомлення")
    elif message.text == "/start":
        start(message)
    else:
        if message.text != "Все з маленької" and message.text != "ВСЕ З МАЛЕНЬКОЇ" and message.text != "Все з великої" and message.text != "ВСЕ З ВЕЛИКОЇ":
            bot.send_message(message.chat.id, message.text.upper())


bot.polling(none_stop=True)