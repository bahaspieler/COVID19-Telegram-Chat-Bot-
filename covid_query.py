import telebot
import requests
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import pandas as pd
import time




def get_country_name(search_key):
    key = ReplyKeyboardMarkup(row_width=3, resize_keyboard=False, one_time_keyboard=False)
    r = requests.get('will be given when the bot will be up for production')
    data = json.loads(r.content)
    countries = [i['name'] for i in data['countries']]
    print(len(countries))
    button_list =[]
    # countries.insert(0, 'BACK')
    back_button= KeyboardButton('BACK')
    key.add(back_button)
    key.add(*[KeyboardButton(str(i)) for i in countries])

    return key, countries

def get_country_notify(search_key):
    key = ReplyKeyboardMarkup(row_width=3, resize_keyboard=False, one_time_keyboard=False)
    r = requests.get('will be given when the bot will be up for production')
    data = json.loads(r.content)
    countries = [i['name'] for i in data['countries']]
    print(len(countries))
    button_list =[]
    # countries.insert(0, 'BACK')
    back_button= KeyboardButton('BACK')
    clear_button = KeyboardButton('Clear All')
    key.add(back_button, clear_button)
    key.add(*[KeyboardButton(str(i)) for i in countries])

    return key, countries

