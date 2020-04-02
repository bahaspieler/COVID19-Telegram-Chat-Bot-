from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from .models import bot_user, first_button, country_update
import requests
from time import time
from tabulate import tabulate
from dateutil.parser import parse
from datetime import datetime
# Create your views here.

bot_token = 'your bot token'
hotline= ['+333', '+10655', '+16263']

def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False




class FirstButtons(APIView):
    def get(self, request):

        data = {'list': []}
        field = list(first_button.objects.all().values('buttons'))
        for i in field:
            data['list'].append({'name': i['buttons']})
        return Response(data)

    def post(self, request):
        data = json.loads(request.body)
        user_name = data['first_name']
        user_id = data['from_user']
        print(user_name)

        if list(bot_user.objects.filter(user_name = user_name, user_id = user_id))==[]:
            bot_user.objects.create(user_name = user_name, user_id = user_id)
        return Response(data)


class QueryResult(APIView):
    def post(self, request):
        data = json.loads(request.body)
        print(data)
        user_name = data['first_name']
        user_id = data['from_user']
        message = data['text']
        query_catagory_list = list(first_button.objects.all().values_list('buttons', flat=True))
        print(query_catagory_list)


        if message in query_catagory_list:
            print("got into the update loop")
            bot_user.objects.filter(user_name=user_name, user_id=user_id).update(query = message)
            text=message
            if message == query_catagory_list[0]:
                r_sum= requests.get('will be released when the bot will be up for production')
                data_sum = json.loads(r_sum.content)
                #summary_confirmed=data['confirmed']['value']
                r_coun=requests.get('will be released when the bot will be up for production')
                data_coun = json.loads(r_coun.content)
                countries_tot = len([i['name'] for i in data_coun['countries']])
                text_sum= [['Confirmed', data_sum['confirmed']['value']],['Recovered',  data_sum['recovered']['value']],
                           ['Deaths', data_sum['deaths']['value']],['Affected Countries', countries_tot]]

                final = {'text': text_sum, 'code': 113}
            elif message == query_catagory_list[1]:
                final = {'text': text,'code': 111}
            elif message == query_catagory_list[2]:
                final = {'text': text, 'code': 112}

            elif message == query_catagory_list[3]:
                final = {'text': text, 'code': 114}

            elif message == query_catagory_list[4]:
                 final = {'text': text, 'code': 911 }


        elif message =='BACK':
            text = 'get back'
            final = {'text': text, 'code': 999}

        # elif message == 'Clear All':
        #     pass

        else:
            if bot_user.objects.filter(user_name=user_name, user_id=user_id).values_list('query', flat=True)[0] == query_catagory_list[1]:
                print('query: ', bot_user.objects.filter(user_name=user_name, user_id=user_id).values_list('query', flat=True))
                message= message.capitalize()
                print(message)
                try:
                    r = requests.get('will be released when the bot will be up for production'.format(message))
                    data = json.loads(r.content)
                    # confirmed = data['confirmed']
                    # deaths = data['deaths']
                    if len(data) > 1:
                        #data_prov = json.loads(r.content)
                        country_region = data[0]['country']
                        active = sum([i['active'] for i in data])
                        r_main = requests.get('will be released when the bot will be up for production'.format(message))
                        data_main = json.loads(r_main.content)
                        confirmed = data_main['confirmed']['value']
                        recovered = data_main['recovered']['value']
                        deaths = data_main['deaths']['value']

                        # confirmed = sum([i['confirmed'] for i in data_prov])
                        # recovered = sum([i['recovered'] for i in data_prov])
                        # deaths = sum([i['deaths'] for i in data_prov])
                        text = [['Country', country_region],['confirmed', confirmed],['recovered', recovered], ['deaths', deaths],['active', active]]
                    else:
                        desired_keys = ['country', 'confirmed', 'recovered', 'deaths', 'active']
                        data_tuple = list(data[0].items())
                        #print(data_tuple)
                        text = [list(ele) for ele in data_tuple if ele[0] in desired_keys]
                        text[0][0] = 'Country'
                    print(text)

                    final = {'text': text, 'code': 222}
                except:
                    text = [['Not Found', 'Please check your spelling!!']]
                    final = {'text': text, 'code': 220}

            elif bot_user.objects.filter(user_name=user_name, user_id=user_id).values_list('query', flat=True)[0] == query_catagory_list[2]:

                if list(bot_user.objects.filter(user_name=user_name, user_id=user_id).values_list('country_notif', flat=True))==['']:
                    bot_user.objects.filter(user_name=user_name, user_id=user_id).update(country_notif =message)
                    text = 'Selected Country:\n{}'.format(message)
                    final = {'text': text, 'code': 888}
                else:
                    if message == 'Clear All':
                        bot_user.objects.filter(user_name=user_name, user_id=user_id).update(country_notif='')
                        text = 'Notification filters are cleared.'
                        final = {'text': text, 'code': 888}
                    else:
                        country_string = bot_user.objects.filter(user_name=user_name, user_id=user_id).values_list('country_notif', flat=True)[0]
                        country_list= country_string.split('-')


                        country_list.append(message)

                        print(country_list)
                        country_list_unq = list(set(country_list))
                        text = 'Selected Countries:\n{}'.format(',  '.join(country_list_unq))

                        country_update = '-'.join(country_list)
                        bot_user.objects.filter(user_name=user_name, user_id=user_id).update(country_notif=country_update)
                        final={'text': text, 'code': 888}

            elif bot_user.objects.filter(user_name=user_name, user_id=user_id).values_list('query', flat=True)[0] ==query_catagory_list[3]:
                if is_date(message) == False:
                    bot_user.objects.filter(user_name=user_name, user_id=user_id).update(date_country=message)
                    text = 'Please give the date. The format must be YYYY-MM-DD'
                    final = {'text': text, 'code': 2020}
                else:
                    date_country = bot_user.objects.filter(user_name=user_name, user_id=user_id).values_list('date_country',
                                                                                              flat=True)[0]
                    print('date_country', date_country)
                    if message == datetime.today().strftime('%Y-%m-%d'):
                        r = requests.get('will be released when the bot will be up for production'.format(date_country))
                        data = json.loads(r.content)
                        # confirmed = data['confirmed']
                        # deaths = data['deaths']
                        if len(data) > 1:
                            # data_prov = json.loads(r.content)
                            country_region = data[0]['country']
                            active = sum([i['active'] for i in data])
                            r_main = requests.get('will be released when the bot will be up for production'.format(date_country))
                            data_main = json.loads(r_main.content)
                            confirmed = data_main['confirmed']['value']
                            recovered = data_main['recovered']['value']
                            deaths = data_main['deaths']['value']

                            # confirmed = sum([i['confirmed'] for i in data_prov])
                            # recovered = sum([i['recovered'] for i in data_prov])
                            # deaths = sum([i['deaths'] for i in data_prov])
                            text = [['Country', country_region], ['confirmed', confirmed], ['recovered', recovered],
                                    ['deaths', deaths], ['active', active]]
                        else:
                            desired_keys = ['country', 'confirmed', 'recovered', 'deaths', 'active']
                            data_tuple = list(data[0].items())
                            # print(data_tuple)
                            text = [list(ele) for ele in data_tuple if ele[0] in desired_keys]

                        final = {'text': text, 'code': 2021}
                    else:

                        try:
                            r = requests.get('will be released when the bot will be up for production'.format(message))
                            data = json.loads(r.content)
                            confirmed = sum([int(i['confirmed']) for i in data if i['country'] == date_country])
                            recovered = sum([int(i['recovered']) for i in data if i['country'] == date_country])
                            active = sum([int(i['active']) for i in data if i['country'] == date_country])
                            deaths = sum([int(i['deaths']) for i in data if i['country'] == date_country])
                            if confirmed == 0 and recovered == 0 and active == 0  and deaths == 0:
                                text = 'Please give the right input format.\nAnd make sure that you are not querying from the future or way past.!!!'  #Any changes her should be done in covid_bot.py also
                            else:
                                if date_country != 'US':
                                    text = [['Country', date_country], ['confirmed', confirmed], ['recovered', recovered],
                                            ['deaths', deaths], ['active', active]]
                                else:
                                    text = [['Country', date_country], ['confirmed', confirmed], ['recovered', recovered],
                                            ['deaths', deaths]]
                            final = {'text': text, 'code': 2021}
                        except:
                            text ='Data can not be fetched.\nPlease re-check the date format (YYYY-MM-DD) !!'
                            final = {'text': text, 'code': 2021}
        return Response(final)

class NotificationInfo(APIView):
    def get(self, request):
        data = {'list': []}
        notify_info = bot_user.objects.all().values('user_id', 'country_notif')

        notify_countries = list(bot_user.objects.all().values_list('country_notif', flat= True))
        notify_countries_list = list(set([j for i in notify_countries for j in i.split('-') if j!= '']))
        start = time()
        for country in notify_countries_list:
            print('Country --->', country)
            r = requests.get('will be released when the bot will be up for production'.format(country))
            data = json.loads(r.content)
            if len(data) > 1:
                #data_prov = json.loads(r.content)
                country_region = data[0]['country']
                active = sum([i['active'] for i in data])
                r_main = requests.get('will be released when the bot will be up for production'.format(country))
                data_main = json.loads(r_main.content)
                confirmed = data_main['confirmed']['value']
                recovered = data_main['recovered']['value']
                deaths = data_main['deaths']['value']
                data_list = [['country', country_region], ['confirmed', confirmed], ['recovered', recovered],
                        ['deaths', deaths], ['active', active]]
            else:
                desired_keys = ['country', 'confirmed', 'recovered', 'deaths', 'active']
                data_tuple = list(data[0].items())
                data_list = [list(ele) for ele in data_tuple if ele[0] in desired_keys]
            data_str = json.dumps(data_list)
            #print(data_str)

            if list(country_update.objects.filter(name=country)) == []:
                country_update.objects.create(name=country, info=data_str)
            else:
                # print("got into else block for:", country)
                if country_update.objects.filter(name= country).values_list('info', flat=True)[0] != data_str:
                    pre_data = json.loads(country_update.objects.filter(name=country).values_list('info', flat=True)[0])
                    print("Getting updated for:", country)
                    data_column = ['', 'Total', 'New Cases']
                    data_blank = ['', '', '']
                    data_send = data_list

                    for i in range(len(data_list)):
                        if type(pre_data[i][1]) is str:
                            data_send[i].append('')
                        if type(pre_data[i][1]) is not str:
                            delt = data_list[i][1] - pre_data[i][1]
                            if delt > 0:
                                data_send[i].append('%2b{:d}'.format(delt))
                            elif delt == 0:
                                data_send[i].append('')
                            elif delt < 0:
                                data_send[i].append('{:-d}'.format(delt))
                    data_send.insert(1, data_column)
                    data_send.insert(1, data_blank)
                    data_send.insert(3, ['', '-----', '---------'])
                    for i in notify_info:
                        user_country = i['country_notif'].split('-')
                        if country in user_country:
                            print("send message block for:", country)
                            message = "<pre>{}</pre>".format(tabulate(data_send, showindex=False))
                            title = 'Latest Update for:  <b><i>{}</i></b>'.format(country)
                            send_title = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + str(i['user_id']) + '&parse_mode=HTML&text=' + title
                            send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + str(i['user_id']) + '&parse_mode=HTML&text=' + message
                            requests.get(send_title)
                            requests.get(send_text)
                    country_update.objects.filter(name= country).update(info = data_str)


        end = time()
        print('For loop time elapsed: ', end-start)
        return Response(notify_info)