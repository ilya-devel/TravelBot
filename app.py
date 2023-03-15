import time
from get_key import get_key
import telebot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from msg import *

KEY = get_key()
bot = telebot.TeleBot(KEY)
BEGIN = ''


@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("Начинаем")
    markup.add(btn1)
    bot.send_message(message.chat.id, welcome, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def start_quiz(message):
    global BEGIN
    BEGIN = time.time()
    if message.text == 'Начинаем':
        markup = get_qst_and_keyboard(cold_heat_list, f'quest_cold_heat')
        bot.send_message(message.from_user.id, quest_cold_heat, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def quest_active_cold(call):
    if call.data == f'{cold_heat_list[0]}_quest_cold_heat':
        markup = get_qst_and_keyboard(yes_no_list, f'cold_active')
        bot.send_message(call.from_user.id, quest_active, reply_markup=markup)

    elif call.data == f'{yes_no_list[0]}_cold_active':
        msg = f'Можешь отправится в одну из этих стран: {" ".join(winter_active_countries)}'
        bot.send_message(call.from_user.id, msg)
        get_all_time(BEGIN, call)



def get_qst_and_keyboard(type_ans, key_qst):
    keys = InlineKeyboardMarkup()
    for key in type_ans:
        keys.add(InlineKeyboardButton(key, callback_data=f'{key}_{key_qst}'))
    return keys


def get_all_time(begin, call):
    tmr = (time.time() - begin)
    msg = f'Я подсказал тебе страну для отдыха за {tmr} секунд'
    bot.send_message(call.from_user.id, msg)


bot.infinity_polling()
# while True:
#     try:
#         bot.polling(non_stop=True)
#     except Exception as err:
#         print(err)
