import secrets
import telebot
from telebot import types
import os
from random import choice
import sqlite3
import threading

lock = threading.Lock()

with open("Config\Токен.txt") as f:
    token = f.readline()

bot = telebot.TeleBot(token)

with open("Config\Ссылка на отзывы.txt") as f:
    link = f.readline()

with open("Config\Юзернейм тех.поддержки.txt") as f:
    link_support = f.readline()

with open("Config\Реквизиты.txt") as f:
    pay = f.readline()


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🖤 Пробник")
    btn3 = types.KeyboardButton("❤️ Прайс-лист")
    btn2 = types.KeyboardButton("💜 Отзывы")
    btn4 = types.KeyboardButton("💼 Тех. поддержка")
    markup.add(btn1, btn3, btn2, btn4)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Что желаешь здесь найти? 💋".format(message.from_user),
                     reply_markup=markup)


s = os.listdir('Source')


@bot.message_handler(content_types=['text'])
def func(message):
    global cursor
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Отзывы", url=link)
    markup.add(button1)

    markup2 = types.InlineKeyboardMarkup()
    button2 = types.InlineKeyboardButton(text='Покупка', callback_data='first')
    markup2.add(button2)

    if message.text == "❤️ Прайс-лист":
        bot.send_message(message.chat.id, text="Прайс-лист: \n\n1. Текст\n2. Текст\n3. Текст\nи т.д",
                         reply_markup=markup2)

    if message.text == "💜 Отзывы":
        bot.send_message(message.chat.id, text="⬇️ Тут будут находиться все отзывы ⬇️", reply_markup=markup)

    if message.text == "💼 Тех. поддержка":
        text = "Единственная техническая поддержка:\n" + link_support
        bot.send_message(message.chat.id, text=text, disable_web_page_preview=True)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY)')
    conn.commit()

    if message.text == "🖤 Пробник":

        user_id = message.chat.id

        with lock:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
            result = cursor.fetchone()

            if result:
                bot.send_message(message.chat.id, text="Ты уже получал свой пробник. 🥺")
            else:
                send = bot.send_message(message.chat.id, text="Твой пробник:")
                for i in range(len(s)):
                    source = open('Source/' + s[i], 'rb')
                    bot.send_photo(message.chat.id, source)
                cursor.execute("INSERT INTO users (id) VALUES (?)", (user_id,))
                conn.commit()

            conn.close()


@bot.callback_query_handler(func=lambda call: True)
def step2(call):
    menu2 = telebot.types.InlineKeyboardMarkup()
    menu2.add(telebot.types.InlineKeyboardButton(text='Текст 1', callback_data='3f'))
    menu2.add(telebot.types.InlineKeyboardButton(text='Текст 2', callback_data='4f'))
    menu2.add(telebot.types.InlineKeyboardButton(text='Текст 3', callback_data='5f'))
    menu2.add(telebot.types.InlineKeyboardButton(text='Текст 4', callback_data='6f'))
    menu2.add(telebot.types.InlineKeyboardButton(text='Текст 5', callback_data='7f'))

    menu3 = telebot.types.InlineKeyboardMarkup()
    menu3.add(telebot.types.InlineKeyboardButton(text='Проверить', callback_data='8f'))

    if call.data == 'first':
        bot.send_message(call.message.chat.id, 'Что вы хотите купить?', reply_markup=menu2)

    list_generic = "A a B b C c D d E e F f G g H h I i J j K k L l M m N n O o P p Q q R r S s T t U u V v W w X x Y y Z z 1 2 3 4 5 6 7 8 9".split()

    generic_length = 20

    generic = ''
    for i in range(generic_length):
        generic += ''.join(secrets.choice(list_generic))

    if call.data == '3f':
        text = "Оплата: 🥝QIWI-кошелёк\n\n💳Сумма: <сумма>\n💬Комментарий: " + generic + "\n📞Номер: " + pay + "\n\n⛔️ Обязательно оставляйте комментарей к платежу. ⛔️"
        bot.send_message(call.message.chat.id, text=text, reply_markup=menu3)
    if call.data == '4f':
        text = "Оплата: 🥝QIWI-кошелёк\n\n💳Сумма: <сумма>\n💬Комментарий: " + generic + "\n📞Номер:\n" + pay + "\n\n⛔️ Обязательно оставляйте комментарей к платежу. ⛔️"
        bot.send_message(call.message.chat.id, text=text, reply_markup=menu3)
    if call.data == '5f':
        text = "Оплата: 🥝QIWI-кошелёк\n\n💳Сумма: <сумма>\n💬Комментарий: " + generic + "\n📞Номер: " + pay + "\n\n⛔️ Обязательно оставляйте комментарей к платежу. ⛔️"
        bot.send_message(call.message.chat.id, text=text, reply_markup=menu3)
    if call.data == '6f':
        text = "Оплата: 🥝QIWI-кошелёк\n\n💳Сумма: <сумма>\n💬Комментарий: " + generic + "\n📞Номер: " + pay + "\n\n⛔️ Обязательно оставляйте комментарей к платежу. ⛔️"
        bot.send_message(call.message.chat.id, text=text, reply_markup=menu3)
    if call.data == '7f':
        text = "Оплата: 🥝QIWI-кошелёк\n\n💳Сумма: <сумма>\n💬Комментарий: " + generic + "\n📞Номер: " + pay + "\n\n⛔️ Обязательно оставляйте комментарей к платежу. ⛔️"
        bot.send_message(call.message.chat.id, text=text, reply_markup=menu3)

    if call.data == '8f':
        text = "Платёж не найден."
        bot.send_message(call.message.chat.id, text=text)


threads = []
for i in range(10):
    t = threading.Thread(args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

bot.polling(none_stop=True)
