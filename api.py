import threading

from fastapi import FastAPI

from api_models import TelegramUpdate
from classes import Message
from services.bot import Bot, CampusBot

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


def read_unad_email(_):
    bot = CampusBot()
    thread = threading.Thread(target=bot.send_unread_emails)
    thread.start()


COMMANDS = {"/readunademail": read_unad_email}


@app.post("/hook")
def recieve_telegram_message(data: TelegramUpdate):
    bot = Bot()

    if data.callback_query:
        bot.send_message("Ese boton no hace nada")
        return {}
        # message_content = data.callback_query.data

    message_content = data.message.text

    if message_content.startswith("/"):
        command = COMMANDS.get(message_content.split(" ")[0])
        if not command:
            bot.send_message("Ese comando no está")
            return {}

        command(message_content)
        return {}

    response = bot.ask_gemini(message_content)
    bot.send_message(response)
    return {}


@app.post("/send-message")
def recieve_telegram_message(data: Message):
    bot = CampusBot()
    bot.send_message(data.text)
    return {}
