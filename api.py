from fastapi import FastAPI
from pydantic import BaseModel

from services.bot import Bot, CampusBot

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


class Message(BaseModel):
    text: str


class TelegramUpdate(BaseModel):
    message: Message


def read_unad_email(_):
    bot = CampusBot()
    bot.send_unread_emails()


COMMANDS = {"/readunademail": read_unad_email}


@app.post("/hook")
def recieve_telegram_message(data: TelegramUpdate):
    bot = Bot()
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


@app.post("/read-campus-email")
def recieve_telegram_message(data: Message):
    bot = CampusBot()
    bot.send_unread_emails()
    return {}
