import time
from random import choice
from classes import User
from get_key import get_key
import telebot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from msg import *

KEY = get_key()
bot = telebot.TeleBot(KEY)
LST_USER = dict()


@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("Начинаем")
    markup.add(btn1)
    bot.send_message(message.chat.id, welcome, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def start_quiz(message):
    LST_USER[message.from_user.id] = User(message.from_user.id)
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
        get_all_time(call)

    elif call.data == f'{yes_no_list[1]}_cold_active':
        markup = get_qst_and_keyboard(yes_no_list, f'qst_grenl')
        bot.send_message(call.from_user.id, quest_grenland, reply_markup=markup)

    elif call.data == f'{yes_no_list[0]}_qst_grenl':
        msg = f'Присмотрись к курортам России, например Байкал или Архангельск'
        bot.send_message(call.from_user.id, msg)
        get_all_time(call)

    elif call.data == f'{yes_no_list[1]}_qst_grenl':
        msg = f'Отлично, я думаю, что это идеальный вариант для вас.'
        bot.send_message(call.from_user.id, msg)
        get_all_time(call)

    elif call.data == f'{cold_heat_list[1]}_quest_cold_heat':
        markup = get_qst_and_keyboard(yes_no_list, f'heat_active')
        bot.send_message(call.from_user.id, quest_active, reply_markup=markup)

    elif call.data == f'{yes_no_list[0]}_heat_active':
        markup = get_qst_and_keyboard(yes_no_list, 'quest_trip_history')
        bot.send_message(call.from_user.id, quest_trip_history, reply_markup=markup)

    elif call.data == f'{yes_no_list[0]}_quest_trip_history':
        markup = get_qst_and_keyboard(in_tur_list, 'quest_private_tour')
        bot.send_message(call.from_user.id, quest_private_tour, reply_markup=markup)

    elif call.data == f'{in_tur_list[0]}_quest_private_tour':
        LST_USER[call.from_user.id].lst_country += individ_list
        do_choice(call)

    elif call.data == f'{in_tur_list[1]}_quest_private_tour':
        LST_USER[call.from_user.id].lst_country += tur_list
        do_choice(call)

    elif call.data == f'{yes_no_list[1]}_quest_trip_history':
        markup = get_qst_and_keyboard(yes_no_list, 'quest_trip_exotic')
        bot.send_message(call.from_user.id, quest_trip_exotic, reply_markup=markup)

    elif call.data == f'{yes_no_list[0]}_quest_trip_exotic':
        markup = get_qst_and_keyboard(yes_no_list, 'quest_has_vaxine')
        bot.send_message(call.from_user.id, quest_has_vaxine, reply_markup=markup)

    elif call.data == f'{yes_no_list[0]}_quest_has_vaxine':
        LST_USER[call.from_user.id].lst_country += vac_list
        do_choice(call)

    elif call.data == f'{yes_no_list[1]}_quest_has_vaxine':
        LST_USER[call.from_user.id].lst_country += not_vac_list
        do_choice(call)

    elif call.data == f'{yes_no_list[1]}_quest_trip_exotic':
        markup = get_qst_and_keyboard(sea_mountains_list, 'quest_sea_climb')
        bot.send_message(call.from_user.id, quest_sea_climb, reply_markup=markup)

    elif call.data == f'{sea_mountains_list[0]}_quest_sea_climb':
        LST_USER[call.from_user.id].lst_country += sea_list
        do_choice(call)

    elif call.data == f'{sea_mountains_list[1]}_quest_sea_climb':
        markup = get_qst_and_keyboard(yes_no_list, 'quest_has_visa')
        bot.send_message(call.from_user.id, quest_has_visa, reply_markup=markup)

    elif call.data == f'{yes_no_list[0]}_quest_has_visa':
        markup = get_qst_and_keyboard(yes_no_list, 'quest_has_child')
        bot.send_message(call.from_user.id, quest_has_child, reply_markup=markup)

    elif call.data == f'{yes_no_list[0]}_quest_has_child':
        markup = get_qst_and_keyboard(age_of_children, 'quest_child_age')
        bot.send_message(call.from_user.id, quest_child_age, reply_markup=markup)

    elif call.data.endswith('quest_child_age'):

        num = int(call.data.split("_")[0])
        print(num)

        if 0 <= num < 4:
            LST_USER[call.from_user.id].lst_country += little_children
            do_choice(call)

        if 3 < num < 18:
            markup = get_qst_and_keyboard(yes_no_list, 'quest_pay_child')
            bot.send_message(call.from_user.id, quest_pay_child, reply_markup=markup)

    elif call.data == f'{yes_no_list[0]}_quest_pay_child':
        LST_USER[call.from_user.id].lst_country += pay_for_children
        do_choice(call)

    elif call.data == f'{yes_no_list[1]}_quest_pay_child':
        LST_USER[call.from_user.id].lst_country += not_pay_for_children
        do_choice(call)

    elif call.data == f'{yes_no_list[1]}_quest_has_child':
        LST_USER[call.from_user.id].lst_country += without_children_list
        do_choice(call)

    elif call.data == f'{yes_no_list[1]}_quest_has_visa':
        LST_USER[call.from_user.id].lst_country += not_visa_list
        do_choice(call)

    elif call.data == f'{yes_no_list[1]}_heat_active':
        LST_USER[call.from_user.id].lst_country += passive_relax
        do_choice(call)

    elif call.data == f'was_{yes_no_list[1]}':
        bot.send_message(call.from_user.id, 'Отлично, я думаю, что это идеальный вариант для вас.')
        get_all_time(call)

    elif call.data == f'was_{yes_no_list[0]}':
        do_choice(call)


def get_qst_and_keyboard(type_ans, key_qst):
    keys = InlineKeyboardMarkup()
    if len(type_ans) < 3:
        for key in type_ans:
            keys.add(InlineKeyboardButton(key, callback_data=f'{key}_{key_qst}'))
        return keys
    else:
        for key_row in [type_ans[i * 5:i * 5 + 5] for i in range(len(type_ans) % 5)]:
            print(key_row)
            btns = [InlineKeyboardButton(key, callback_data=f'{key}_{key_qst}') for key in key_row]
            keys.row(*btns)
        return keys


def do_choice(call):
    if len(LST_USER[call.from_user.id].lst_country) > 0:
        country = choice(LST_USER[call.from_user.id].lst_country)
        LST_USER[call.from_user.id].lst_country.remove(country)
        msg = f'Что насчет {country}. Был ли ты там?'
        keys = InlineKeyboardMarkup(row_width=2)
        for key in yes_no_list:
            keys.add(InlineKeyboardButton(key, callback_data=f'was_{key}'))
        bot.send_message(call.from_user.id, msg, reply_markup=keys)
    else:
        bot.send_message(call.from_user.id, 'Извини, идеи закончились :(')
        get_all_time(call)


def get_all_time(call):
    tmr = (time.time() - LST_USER[call.from_user.id].begin)
    msg = f'Я подсказал тебе страну для отдыха за {"%.02f" % tmr} секунд'
    bot.send_message(call.from_user.id, msg)


bot.infinity_polling()
# while True:
#     try:
#         bot.polling(non_stop=True)
#     except Exception as err:
#         print(err)
