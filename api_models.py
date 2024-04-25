from typing import Optional
from pydantic import BaseModel


class Message(BaseModel):
    text: str


class CallbackQuery(BaseModel):
    data: str


class TelegramUpdate(BaseModel):
    message: Optional[Message] = None
    callback_query: Optional[CallbackQuery] = None
