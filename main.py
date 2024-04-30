import os
import telebot
from telebot import types
import datetime
import numpy as np

current_date_time = datetime.datetime.now()
current_time = current_date_time.time()
print('start', current_time)
token = '7105704391:AAHXkjwwTRaQB-7z5qiTa1nnU1qGRgwbC9k'
bot = telebot.TeleBot(token)

# Храним систему линейных уравнений
equations = []
flag = True
keyboard = types.ReplyKeyboardMarkup()
keyboard_btn1 = (types.KeyboardButton('solve'))
keyboard_btn2 = (types.KeyboardButton('clear_all'))
keyboard_btn3 = (types.KeyboardButton('delete_prev'))
keyboard_btn4 = (types.KeyboardButton('help'))


# Определяем обработчик команды start
@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup()
    markup.row(keyboard_btn1, keyboard_btn2, keyboard_btn3, keyboard_btn4)
    bot.send_message(message.chat.id,
                     f'Добро пожаловать, {str(message.from_user.first_name).capitalize()}, в Happy Math!',
                     reply_markup=markup)


@bot.message_handler()
def txt(message):
    if message.text == 'help':
        bot.send_message(message.chat.id,
                         """Я - бот, который может решить систему линейных уравнений, используя метод Гаусса. Я только даю вам ответ. Но скоро я смогу показать само решение.

Для того чтобы я смог решить систему уравнений необходимо ее правильно ввести.
Сначала мне необходимо знать порядок переменных.
Для этого вы должны мне их передать в сообщении: order <кол-во переменных> <буквы или слова(словосочетания, но без пробеллов), которыми обозначаются переменные переменные вводятся через ОДИН ПРОБЕЛЛ>.
Ввод частей системы уравнений выполняется построчно, но уже с коэффицентами, важно также помнить что свободный член необходимо разместить последним.
После ввода строки система вам предложит нажать на кнопку add чтобы подтвердить ввод. Если же вы ввели уравнение с ощибкой, то вам необходимо просто заново его ввести.

Например:
Нам дана система состоящая из 2 уравнений:
1) 5x + 2y + s = 11
2) 4u + 3y + 2s - 9 = 12
Как нужно вводить уравнение:
order 4 x y u s
5 2 0 1 11
0 3 4 2 3

Чтобы решеить уравнение вам необходимо нажать на клавиатуре кнопку solve. После этого программа проверит что вы предоставили корректные данные и предложит вам или ответ к поставленной или попросит ввести корректное уравнение.
Чтобы удалить предущее уравнение в системе необходимо нажать на кнопку delete_prev
Чтобы удалить всю систему уравнений необходимо нажать на кнопку clear_all
ЧТобы посмотреь на уже введенную матрицу необходимо написать в чат print
Бот не несет ответственности за неправильно введенное или непроверенное уравнение, он все таки не человек.
Также пока не умеет решать системы в которых переменные могу принимать бесконечное множество значений.
""")
        with open('help', 'r', encoding='utf-8') as f:
            data = f.read().splitlines()
            print(data)
    elif message.text == 'print':
        if len(equations):
            s = ''
            for i in equations:
                s += i + '\n'
            bot.send_message(message.chat.id, s)
        else:
            bot.send_message(message.chat.id, 'Вы ничего не ввели.')
    elif message.text == 'solve':
        with open('order.txt', 'r') as f:
            order = f.read().splitlines()
        cnt = int(order[0])
        sp = list(set(order[1].split()))
        if len(equations) and cnt == len(sp):
            bot.send_message(message.chat.id, 'Решаем систему...')
            try:
                with open('start_system.txt', 'w') as f:
                    for i in equations:
                        print(i, file=f)
                with open('start_system.txt', 'r', encoding='utf-8') as f:
                    data = f.read().splitlines()
                    n = len(data)
                    sp1 = []
                    sp2 = []
                    for i in range(n):
                        sp = [int(x) for x in data[i].split()]
                        sp2.append(sp[-1])
                        del sp[-1]
                        sp1.append(sp)
                    A = np.array(sp1)
                    b = np.array(sp2)
                x = np.linalg.solve(A, b)
                with open('order.txt', 'r', encoding='utf-8') as f:
                    order = f.read().split()
                with open('output.txt', 'w', encoding='utf-8') as f:
                    for i in range(1, len(order)):
                        print(f'{order[i]} = {x[i - 1]}', file=f)
                with open('output.txt', 'r') as f:
                    output = f.read().splitlines()
                    bot.send_message(message.chat.id, '\n'.join(output))
            except Exception as e:
                bot.send_message(message.chat.id, 'Пожалуйста проверьте корректность введенных данных;)')
        else:
            bot.send_message(message.chat.id, 'Пожалуйста проверьте корректность введенных данных;)')
    elif message.text == 'clear_all':
        with open('start_system.txt', 'w') as f:
            f.truncate(0)
        with open('order.txt', 'w') as f:
            f.truncate(0)
        equations.clear()
        bot.send_message(message.chat.id, 'Все было удалено.')
    elif 'order' in message.text.split(' '):
        order = str(message.text).split(' ')
        with open('order.txt', 'w') as f:
            print(order[1], file=f)
            for i in range(2, len(order)):
                print(order[i], end=' ', file=f)
        bot.send_message(message.chat.id, 'Сделано')
        equations.clear()
    elif message.text == 'delete_prev':
        if len(equations) == 0:
            bot.send_message(message.chat.id, 'Не осталось ниего, что можно было бы удалить')
        else:
            del equations[-1]
            bot.send_message(message.chat.id, 'Готово')
    else:
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('add', callback_message=message.text, callback_data='add')
        markup.row(btn1)
        bot.send_message(message.chat.id, message.text, reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'add':
        equations.append(callback.message.text)
        bot.send_message(callback.message.chat.id, 'Добавлено')


bot.polling()
