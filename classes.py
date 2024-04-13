from dataclasses import dataclass


@dataclass
class Message():
    type: str
    text: str
    photo: str | bytes = ''