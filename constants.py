import json
import os

BOT_API_KEY = os.getenv('BOT_API_KEY')
USER_CHAT_ID = os.getenv('BOT_API_KEY')
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_API_KEY}"

#campus
C_ID_USUARIO="1094047"
COOKIES = []
with open('cookies.txt', 'rb') as f:
    COOKIES.extend(json.loads(f.read()))