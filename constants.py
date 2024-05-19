import json
import os

from dotenv import load_dotenv


load_dotenv()

BOT_API_KEY = os.getenv("BOT_API_KEY")
if not BOT_API_KEY:
    raise Exception("Define the bot ApiKey")

USER_CHAT_ID = os.getenv("USER_CHAT_ID")
if not BOT_API_KEY:
    raise Exception("Define the user chat_id")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_API_KEY}"
DB_URL = os.getenv("DB_URL") or ""
NOTION_API_KEY = os.getenv("NOTION_API_KEY", "")

# campus
C_ID_USUARIO = "1094047"
COOKIES = []
try:
    with open("cookies.txt", "rb") as f:
        COOKIES.extend(json.loads(f.read()))
except FileNotFoundError:
    ...
