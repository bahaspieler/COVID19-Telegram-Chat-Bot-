import requests
from time import sleep
while True:
    try:
        r = requests.get('http://127.0.0.1:8080/api/notify')
        print('request sent..')

    except:
        print("request couldn't be get...")

    sleep(300)