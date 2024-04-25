import threading
from services.bot import CampusBot


def read_unad_email(_):
    bot = CampusBot()
    thread = threading.Thread(target=bot.send_unread_emails)
    thread.start()


def read_unad_posts(_):
    bot = CampusBot()
    thread = threading.Thread(target=bot.send_new_posts)
    thread.start()

"""
readunademail - Reads the UNAD campus emails for every active course
readunadposts - Reads the new posts from the courses forums
"""
COMMANDS = {
    "/readunademail": read_unad_email,
    "/readunadposts": read_unad_posts,
}