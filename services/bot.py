import traceback
from typing import List
import requests
from constants import TELEGRAM_API_URL, USER_CHAT_ID
from classes import Message
from models.process import end_process, start_process
from scrapers.campus import Campus
from services.gemini import Gemini


class Bot:
    def send(self, message: Message):
        if message.type == "text":
            return self.send_message(message.text)
        if message.type == "photo":
            return self.send_photo(message.text, message.photo)
        if message.type == "file":
            return self.send_file(message.text, message.photo)
        print("Unknown message type")

    def send_message(self, text: str):
        response = requests.post(
            TELEGRAM_API_URL + "/sendMessage",
            headers={"Content_type": "application/json"},
            data={
                "chat_id": USER_CHAT_ID,
                "text": text,
                # 'parse_mode':fmt
            },
        )
        self.log(response)

    def send_photo(self, msg: str = "", file: bytes = None):
        response = requests.post(
            TELEGRAM_API_URL + "/sendPhoto",
            headers={"Content_type": "multipart/form-data"},
            data={
                "chat_id": USER_CHAT_ID,
                "caption": msg,
            },
            files={"photo": ("img", file)},
        )
        self.log(response)

    def send_file(self, msg: str = "", file: bytes = None):
        """msg: file name"""
        response = requests.post(
            TELEGRAM_API_URL + "/sendDocument",
            headers={"Content_type": "multipart/form-data"},
            data={
                "chat_id": USER_CHAT_ID,
                "caption": "",
            },
            files={"document": (msg, file)},
        )
        self.log(response)

    @staticmethod
    def log(response: requests.Response):
        res = response.json()
        if res.get("ok") and res.get("ok") == True:
            print("Post OK")
        if not res.get("ok") and res.get("ok") == False:
            print(f'Post failed: {res.get("description")}\n\n')

    def ask_gemini(self, something):
        gemini = Gemini()
        return gemini.ask_something(something)

class CampusBot(Bot):

    def send_course_messages(self, course: str, messages: List[Message]):
        self.send(Message("text", "❗️❗️❗️ De {0} hay mensajes".format(course)))
        for message in messages:
            self.send(message)

    def send_unread_emails(
        self,
    ):
        self.send(Message("text", "👀 Buscando mensajes..."))
        status = 0
        process = start_process("Read unad email")
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
                self.send_message("🙌 No hay mensajes")
            status = 1
        except Exception as e:
            status = 2
            traceback.print_exc()
            self.send_message(str(e))
        end_process(process, status)

    def send_new_posts(self):
        self.send(Message("text", "👀 Buscando publicaciones nuevas..."))
        status = 0
        process = start_process("Read unad posts")
        try:
            campus = Campus()
            messages = campus.get_unreaded_posts()
            campus.end()
            messages_count = 0
            for course in messages:
                if len(messages[course]) == 0:
                    continue
                self.send_course_messages(course, messages[course])
                messages_count += 1
            if messages_count == 0:
                self.send_message("✍️ No hay publicaciones")
            status = 1
        except Exception as e:
            status = 2
            traceback.print_exc()
            self.send_message(str(e))
        end_process(process, status)
