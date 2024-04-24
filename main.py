import sys

from services.bot import CampusBot

def main(action: str):
    bot = CampusBot()
    if action == 'read_messages':
        bot.send_unread_emails()
    if action == 'read_posts':
        bot.send_new_posts()

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        import time
        time.sleep(5)
        print('No action provided')
    else:
        main(args[0])

# send_unread_emails()
# send_message()
# def job():
#     # send_message()
#     get_news()
#     print(BOT_API_KEY)

# schedule.every(12).hour.do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)