from covid_query import get_country_name, get_country_notify
import telebot
import requests
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from tabulate import tabulate
import pandas as pd
import time

BOT_INTERVAL = 3
BOT_TIMEOUT = 30

bot = telebot.TeleBot('bot token here')

hotline= ['333', '10655', '16263']


def Button(message):
    link = 'http://127.0.0.1:8080/api/buttons'
    text = {"text": message.text, "from_user": message.from_user.id, "first_name": message.from_user.first_name}
    user_id = {"from_user": message.from_user.id}

    print(user_id)
    print(text)
    user_entry = requests.post(link, data=json.dumps(text))
    r = requests.get('http://127.0.0.1:8080/api/buttons')
    data = json.loads(r.content)
    buttons_first= ['Country']
    key = ReplyKeyboardMarkup(row_width=2 ,resize_keyboard=True, one_time_keyboard=False)
    text = 'Hello {0}. \nPlease choose your query-type by selecting one of the below options.'.format(message.from_user.first_name,)


    key.add(*[KeyboardButton(str(i['name'])) for i in data['list']])
    bot.send_message(message.from_user.id, text, reply_markup=key)

@bot.message_handler(commands=['start'])
def start(message):
    Button(message)

@bot.message_handler(content_types='text')
def Send_Message(message):
    link = 'http://127.0.0.1:8080/api/query'
    text = {"text": message.text, "from_user": message.from_user.id, "first_name": message.from_user.first_name}
    start_t = time.time()
    try:
        r = requests.post(link, data=json.dumps(text))
        data = json.loads(r.text)
        end_t = time.time()
        print('post request time elapsed:', end_t-start_t)
        print(message.from_user.first_name,'-->>', data)

        search_key=text['text']

        if data['code'] == 111:
            start_t = time.time()
            key, countries = get_country_name(search_key)
            end_t = time.time()
            print('country name parse time elapsed:', end_t - start_t)
            print(key)
            bot.send_message(message.from_user.id, "Please choose or write the country name", reply_markup=key)

        if data['code'] == 112:
            key, countries = get_country_notify(search_key)
            bot.send_message(message.from_user.id, "Please choose your preferred countries one by one to get notified of LIVE UPDATES!!", reply_markup=key)

        if data['code'] == 114:
            key, countries = get_country_name(search_key)
            bot.send_message(message.from_user.id,
                             "Please choose the country first. After that you will be asked for the DATE (format: YYYY-MM-DD)",
                             reply_markup=key)

        if data['code'] == 911:
            # key = ReplyKeyboardMarkup(row_width=1, resize_keyboard=False, one_time_keyboard=False)
            # status = '\n'.join(hotline)
            for i in hotline:
                bot.send_message(message.from_user.id, i, parse_mode='Markdown')

        if data['code'] == 222 or data['code'] == 220:
            status = "<pre>{}</pre>".format(tabulate(data['text'], showindex=False))
            bot.send_message(message.from_user.id, status, parse_mode='HTML')

        if data['code'] == 113:
            status = "<pre>{}</pre>".format(tabulate(data['text'], showindex=False))
            bot.send_message(message.from_user.id, status, parse_mode='HTML')

        if data['code'] == 999:
            Button(message)
        if data['code'] == 888:
            bot.send_message(message.from_user.id, data['text'], parse_mode='Markdown')
            requests.get('http://127.0.0.1:8080/api/notify')
        if data['code'] == 2020:
            bot.send_message(message.from_user.id, data['text'], parse_mode='Markdown')
        if data['code'] == 2021:

            if type(data['text']) is str:
                bot.send_message(message.from_user.id, data['text'], parse_mode='HTML')
            else:
                status = "<pre>{}</pre>".format(tabulate(data['text'], showindex=False))
                bot.send_message(message.from_user.id, status, parse_mode='HTML')



    except:
        bot.send_message(message.from_user.id,
                         "Sorry!! The server is currently unreachable. Please try again later.",
                         parse_mode='Markdown')




while True:
    try:
        bot.polling(none_stop=True, interval=BOT_INTERVAL, timeout= BOT_TIMEOUT)
    except Exception:
        bot.stop_polling()
        time.sleep(BOT_TIMEOUT)