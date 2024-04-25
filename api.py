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


@app.post("/hook")
def recieve_telegram_message(data: TelegramUpdate):
    bot = Bot()
    response = bot.ask_gemini(data.message.text)
    bot.send_message(response)
    return {}

@app.post("/read-campus-email")
def recieve_telegram_message(data: Message):
    bot = CampusBot()
    bot.send_unread_emails()
    return {}