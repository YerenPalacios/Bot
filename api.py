from fastapi import FastAPI, Request

from api_models import TelegramUpdate
from classes import Message
from commands import COMMANDS
from services.bot import Bot, CampusBot

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

def check_body(data: dict):
    msg = TelegramUpdate(**data)
    if not msg.message and not msg.callback_query:
        return
    return msg


@app.post("/hook")
async def recieve_telegram_message(request: Request):
    body = await request.json()
    data = check_body(body)
    bot = Bot()

    if not data:
        bot.send_message(str(("Request raro:", request.get("server", "???"), body)))
        return {}

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
