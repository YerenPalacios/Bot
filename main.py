import schedule
import time
import os
import requests

from scrapers.campus import Campus


BOT_API_KEY=os.getenv('BOT_API_KEY')
USER_CHAT_ID=os.getenv('BOT_API_KEY')
TELEGRAM_API_URL=f"https://api.telegram.org/bot{BOT_API_KEY}"

ID_USUARIO="1094047"


def get_courses():
    campus = Campus()
    campus.get_courses()

def get_updates():
    response = requests.post(
        TELEGRAM_API_URL+"/getUpdates",
        headers={'Content_type': 'Application/json'},
        data={
            'chat_id': USER_CHAT_ID,
            'limit': 1,
            'timeout': 5
        }
    )
    print(response.content)

def send_message():
    response = requests.post(
        TELEGRAM_API_URL+"/sendMessage",
        headers={'Content_type': 'Application/json'},
        data={
            'chat_id': '6290970561',
            'text': "Probando 123..."
        }
    )
    print(response.content)

# get_courses()
# send_message()
def job():
    send_message()
    print(BOT_API_KEY)

schedule.every(30).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)