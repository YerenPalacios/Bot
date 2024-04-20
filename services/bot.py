
import traceback
from typing import List
import requests
from constants import TELEGRAM_API_URL
from classes import Message
from scrapers.campus import Campus

class Bot():
    def send(self, message: Message):
        if message.type == "text":
            return self.send_message(message.text)
        if message.type == "photo":
            return self.send_photo(message.text, message.photo)
        print('Unknown message type')

    def send_message(self, text: str):
        response = requests.post(
            TELEGRAM_API_URL+"/sendMessage",
            headers={'Content_type': 'application/json'},
            data={
                'chat_id': '6290970561',
                'text': text,
                # 'parse_mode':fmt
            }
        )
        self.log(response)

    def send_photo(self, msg: str = '', file: bytes = None):
        response = requests.post(
            TELEGRAM_API_URL+"/sendPhoto",
            headers={'Content_type': 'multipart/form-data'},
            data={
                'chat_id': '6290970561',
                'caption': msg,
            },
            files={'photo': ('img', file)}
        )
        self.log(response)

    @staticmethod
    def log(response: requests.Response):
        res = response.json()
        if res.get('ok') and res.get('ok') == True:
            print('Post OK')
        if not res.get('ok') and res.get('ok') == False:
            print(f'Post failed: {res.get("description")}\n\n')


class CampusBot(Bot):

    def send_course_messages(self, course: str, messages: List[Message]):
        self.send(
            Message(
                'text', 
                "❗️❗️❗️ De {0} hay mensajes".format(course)
            )
        )
        for message in messages:
            self.send(message)

    def send_unread_emails(self, ):
        self.send(Message('text', '👀 Buscando mensajes...'))
        try:
            campus = Campus()
            messages = campus.read_courses_email()
            campus.end()
            messages_count = 0
            for course in messages: 
                if len(messages[course]) == 0:
                    continue
                self.send_course_messages(course, messages[course])
                messages_count += 1
            if messages_count == 0:
                self.send_message('🙌 No hay mensajes')
        except Exception as e:
            traceback.print_exc()
            self.send_message(e)


# def get_updates():
#     response = requests.post(
#         TELEGRAM_API_URL+"/getUpdates",
#         headers={'Content_type': 'Application/json'},
#         data={
#             'chat_id': USER_CHAT_ID,
#             'limit': 1,
#             'timeout': 5
#         }
#     )
#     print(response.content)


# def get_news():
#     campus = Campus()
#     return campus.get_unreaded_posts()